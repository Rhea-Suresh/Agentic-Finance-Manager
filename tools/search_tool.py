from duckduckgo_search import DDGS

def search_financial_tips(query: str) -> str:
    """Tool: Searches web for financial advice based on spending patterns."""
    with DDGS() as ddgs:
        results = list(ddgs.text(f"personal finance tips {query}", max_results=3))
    if not results:
        return "No results found."
    tips = "\n".join([f"- {r['title']}: {r['body'][:200]}" for r in results])
    return f"Financial Tips for '{query}':\n{tips}"