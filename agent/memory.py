class ShortTermMemory:
    """Maintains conversation/reasoning context within a session."""
    
    def __init__(self):
        self.history = []  # List of {role, content} dicts
        self.observations = []  # Tool call results
    
    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
    
    def add_observation(self, tool_name: str, result: str):
        entry = f"[Tool: {tool_name}] → {result}"
        self.observations.append(entry)
        self.add_message("tool", entry)
    
    def get_context(self) -> str:
        return "\n".join([f"{m['role'].upper()}: {m['content']}" 
                          for m in self.history])
    
    def clear(self):
        self.history = []
        self.observations = []