# News & Hugging Face sentiment agent

# backend/src/agents/sentiment.py
from typing import Dict, Any
from langchain_tavily import TavilySearch
from src.state import FinancialState

# Using the updated tool class
search_tool = TavilySearch(max_results=3)

def news_research_node(state: FinancialState) -> Dict[str, Any]:
    ticker = state["ticker"]
    print(f"\n⚡ [Node: News Research] Activating for {ticker}...")
    
    query = f"latest financial performance, stock news, and market sentiment for {ticker}"
    
    try:
        # Note: Updated classes use 'invoke', passing a dictionary containing 'query'
        search_results = search_tool.invoke({"query": query})
        print(f"✅ [Node: News Research] Context successfully retrieved.")
        
        # Convert list of results or dict to string format for our raw_news list
        return {"raw_news": [str(search_results)]}
    except Exception as e:
        print(f"❌ [Node: News Research] Tool failed: {str(e)}")
        return {"raw_news": [f"Failed to fetch live news data for {ticker}."]}