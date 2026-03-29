from dotenv import load_dotenv
from agent.finance_agent import FinanceAgent

load_dotenv()

def main():
    agent = FinanceAgent()
    
    print("Personal Finance Agent")
    print("=" * 40)
    
    # Example multi-step goals to demonstrate agentic behavior
    goals = [
        "Analyze my expenses this month, check if I'm within budget, and give me saving tips.",
        "Which spending category am I overspending in? What should I do?",
    ]
    
    for goal in goals:
        print(f"\nGoal: {goal}")
        result = agent.run(goal)
        print(f"\nResult: {result}")

if __name__ == "__main__":
    main()
'''

---

### Step 7 — `.env` file
'''
