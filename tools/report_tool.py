def generate_report(analysis: str, budget_status: str, tips: str) -> str:
    """Tool: Compiles final readable finance report."""
    report = f"""
========================================
     💰 PERSONAL FINANCE REPORT
========================================

📊 EXPENSE ANALYSIS:
{analysis}

📈 BUDGET STATUS:
{budget_status}

💡 FINANCIAL TIPS:
{tips}

========================================
"""
    with open("logs/report_output.txt", "w") as f:
        f.write(report)
    return report