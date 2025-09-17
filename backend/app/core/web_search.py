from tavily import TavilyClient
from .config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def perform_web_search(query: str) -> str:
    """Performs a web search using Tavily and returns a summary."""
    try:
        response = tavily_client.get_search_context(query=query, search_depth="basic")
        return response
    except Exception as e:
        print(f"Web search failed: {e}")
        return "No relevant information found on the web."