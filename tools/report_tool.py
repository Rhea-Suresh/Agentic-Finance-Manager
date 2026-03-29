def generate_report(data: str = "") -> str:
    """Tool: Compiles final readable finance report."""
    report = f"""
========================================
     PERSONAL FINANCE REPORT
========================================

{data}

========================================
"""
    with open("logs/report_output.txt", "w") as f:
        f.write(report)
    return f"Report generated:\n{data}"