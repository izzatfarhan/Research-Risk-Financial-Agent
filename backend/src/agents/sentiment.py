# News & Hugging Face sentiment agent

# backend/src/agents/sentiment.py
from typing import Dict, Any
from langchain_community.tools.tavily_search import TavilyAnswer
from src.state import FinancialState

# Initialize the search tool (Ensure TAVILY_API_KEY is in your .env)
search_tool = TavilyAnswer(max_results=3)

def news_research_node(state: FinancialState) -> Dict[str, Any]:
    """Fetches real-time financial market news for the given ticker."""
    ticker = state["ticker"]
    print(f"\n⚡ [Node: News Research] Activating for {ticker}...")
    
    query = f"latest financial performance, stock news, and market sentiment for {ticker}"
    
    try:
        search_results = search_tool.invoke({"query": query})
        print(f"✅ [Node: News Research] Context successfully retrieved.")
        return {"raw_news": [search_results]}
    except Exception as e:
        print(f"❌ [Node: News Research] Tool failed: {str(e)}")
        return {"raw_news": [f"Failed to fetch live news data for {ticker}."]}