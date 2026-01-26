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
    Industry-grade pharmaceutical market search.
    Orchestrates multiple specific queries to build a comprehensive context.
    """
    # Domain-specific search queries
    queries = [
        f"'{molecule}' market size forecast revenue",
        f"'{molecule}' primary pharmaceutical competitors market share",
        f"'{molecule}' therapeutic landscape and trend analysis",
        f"'{molecule}' pricing trends and reimbursement insights",
        f"'{molecule}' commercial launch and peak sales projections"
    ]
    
    all_results = []
    # Use context managers properly and implement simple retry logic
    for q in queries:
        try:
            # Adding specialized filters like site focus (optional but powerful)
            # e.g. "site:globenewswire.com" or "site:nature.com"
            results = search_web(q, max_results=3)
            if results:
                all_results.extend(results)
        except Exception as e:
            logger.warning(f"Search query failed: {q}. Error: {e}")
            continue
    
    # Deduplicate results based on URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get('href')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)

    # Format results with high signal-to-noise ratio
    formatted = "\n---\n".join([
        f"SOURCE: {r.get('href')}\nTITLE: {r.get('title')}\nCONTENT: {r.get('body')}"
        for r in unique_results[:10]  # Limit to top 10 high-quality results
    ])
    
    if not formatted:
        return "No market data found for the specified molecule."
        
    return formatted
