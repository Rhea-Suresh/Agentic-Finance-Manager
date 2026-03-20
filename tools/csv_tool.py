import pandas as pd
import json

def read_expenses(file_path="data/expenses.csv") -> str:
    """Tool: Reads expense CSV and returns summary string."""
    df = pd.read_csv(file_path)
    summary = df.groupby("category")["amount"].sum().to_dict()
    total = df["amount"].sum()
    return f"Total Spent: ₹{total}\nBy Category: {summary}\nRaw Data:\n{df.to_string()}"

def add_expense(date: str, category: str, amount: float, description: str) -> str:
    """Tool: Adds a new expense entry to CSV."""
    df = pd.read_csv("data/expenses.csv")
    new_row = {"date": date, "category": category, "amount": amount, "description": description}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("data/expenses.csv", index=False)
    return f"Added expense: {description} - ₹{amount} under {category}"

def get_budget() -> str:
    """Tool: Reads budget configuration."""
    with open("data/budget.json") as f:
        budget = json.load(f)
    return str(budget)