def calculate_budget_status(total_spent: float, monthly_budget: float) -> str:
    """Tool: Calculates remaining budget and overspend alerts."""
    remaining = monthly_budget - total_spent
    percent_used = (total_spent / monthly_budget) * 100
    status = "OVERSPENT" if remaining < 0 else " Within Budget"
    return (
        f"Budget Analysis:\n"
        f"  Monthly Budget: ₹{monthly_budget}\n"
        f"  Total Spent: ₹{total_spent}\n"
        f"  Remaining: ₹{remaining}\n"
        f"  Used: {percent_used:.1f}%\n"
        f"  Status: {status}"
    )

def calculate_category_overspend(spent_by_category: dict, limits: dict) -> str:
    """Tool: Checks which categories exceeded limits."""
    alerts = []
    for category, limit in limits.items():
        spent = spent_by_category.get(category, 0)
        if spent > limit:
            alerts.append(f"  {category}: Spent ₹{spent}, Limit ₹{limit} (Over by ₹{spent-limit})")
        else:
            alerts.append(f" {category}: Spent ₹{spent}, Limit ₹{limit}")
    return "Category Status:\n" + "\n".join(alerts)