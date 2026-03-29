import os
import json
import logging
import time
from dotenv import load_dotenv

load_dotenv()  # must be BEFORE OpenAI client

from openai import OpenAI
from agent.memory import ShortTermMemory
from tools.csv_tool import read_expenses, add_expense, get_budget
from tools.calculator_tool import calculate_budget_status, calculate_category_overspend
from tools.search_tool import search_financial_tips
from tools.report_tool import generate_report

# Setup observable logging (required by professor)
logging.basicConfig(
    filename="logs/agent_traces.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

TOOL_MAP = {
    "read_expenses": read_expenses,
    "get_budget": get_budget,
    "search_financial_tips": search_financial_tips,
    "generate_report": generate_report,
}

SYSTEM_PROMPT = """You are a Personal Finance Agent.
You help users understand their spending patterns and give advice.
You follow the ReAct pattern:
THOUGHT: Reason about what to do next
ACTION: Call one of these tools: read_expenses, get_budget, search_financial_tips, generate_report
OBSERVATION: You will receive tool results
... repeat until done ...
FINAL ANSWER: Give a clear, helpful response to the user
Always use at least 3 tool calls before giving a final answer.
Format actions as: ACTION: tool_name | input_if_needed
"""

MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "meta-llama/llama-3.2-3b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
]

def call_llm(messages):
    """Try multiple free models with retry logic."""
    for model in MODELS:
        for attempt in range(3):
            try:
                print(f"  [Using model: {model}]")
                response = client.chat.completions.create(
                    model=model,
                    messages=messages
                )
                return response
            except Exception as e:
                if "429" in str(e):
                    wait = 15 * (attempt + 1)
                    print(f"  Rate limited on {model}, waiting {wait}s... (attempt {attempt+1}/3)")
                    time.sleep(wait)
                elif "404" in str(e) or "400" in str(e):
                    print(f"  Model {model} not available, trying next...")
                    break  # try next model immediately
                else:
                    raise e
    raise Exception("All models exhausted. Please wait a minute and try again.")

class FinanceAgent:
    def __init__(self):
        self.memory = ShortTermMemory()

    def _log(self, step: str, content: str):
        logging.info(f"[{step}] {content}")
        print(f"\n{'='*50}\n[{step}]\n{content}")

    def _call_tool(self, tool_name: str, tool_input: str = "") -> str:
        self._log("TOOL CALL", f"{tool_name}({tool_input})")
        if tool_name not in TOOL_MAP:
            return f"Unknown tool: {tool_name}"
        
        # Ignore empty or invalid inputs like {}, None, empty string
        clean_input = tool_input.strip() if tool_input else ""
        if clean_input in ("", "{}", "none", "None", "null"):
            clean_input = ""
        
        result = TOOL_MAP[tool_name](clean_input) if clean_input else TOOL_MAP[tool_name]()
        self._log("OBSERVATION", result[:300] + "..." if len(result) > 300 else result)
        return result

    def run(self, user_goal: str) -> str:
        self._log("USER GOAL", user_goal)
        self.memory.add_message("user", user_goal)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_goal}
        ]

        for step in range(6):
            response = call_llm(messages)
            agent_output = response.choices[0].message.content
            self._log(f"AGENT STEP {step+1}", agent_output)
            self.memory.add_message("assistant", agent_output)
            messages.append({"role": "assistant", "content": agent_output})

            if "ACTION:" in agent_output:
                action_line = [l for l in agent_output.split("\n") if "ACTION:" in l][0]
                parts = action_line.replace("ACTION:", "").strip().split("|")
                tool_name = parts[0].strip()
                tool_input = parts[1].strip() if len(parts) > 1 else ""

                observation = self._call_tool(tool_name, tool_input)
                self.memory.add_observation(tool_name, observation)
                messages.append({
                    "role": "user",
                    "content": f"OBSERVATION: {observation}\nContinue your reasoning."
                })

            elif "FINAL ANSWER:" in agent_output:
                final = agent_output.split("FINAL ANSWER:")[-1].strip()
                self._log("FINAL ANSWER", final)
                return final

        return "Agent completed maximum reasoning steps. Check logs for full trace."