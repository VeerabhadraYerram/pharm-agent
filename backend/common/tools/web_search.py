from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Searches the web using DuckDuckGo.
    Returns a list of results with 'title', 'href', and 'body'.
    """
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=max_results)]
            return results
    except Exception as e:
        logger.error(f"Search failed for query '{query}': {e}")
        return []

def search_market_info(molecule: str) -> str:
    """
    Specific helper for pharmaceutical market search.
    """
    queries = [
        f"{molecule} pharmaceutical market size competitors",
        f"{molecule} patent expiration date",
        f"{molecule} sales revenue projections"
    ]
    
    all_results = []
    for q in queries:
        all_results.extend(search_web(q, max_results=3))
    
    # Format results for LLM consumption
    formatted = "\n---\n".join([
        f"Title: {r.get('title')}\nSource: {r.get('href')}\nSnippet: {r.get('body')}"
        for r in all_results
    ])
    return formatted
