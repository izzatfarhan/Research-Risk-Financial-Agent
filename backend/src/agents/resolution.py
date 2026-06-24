import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from src.state import FinancialState
from dotenv import load_dotenv

load_dotenv()
THINKING_LEVEL = "medium"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class TickerResolutionSchema(BaseModel):
    ticker: str = Field(description="The exact Yahoo Finance ticker symbol for the requested company or stock. Must include the correct exchange suffix if non-US (e.g., 5347.KL for Tenaga Nasional Berhad, RELIANCE.NS for Reliance). If it is already a valid ticker, return it normalized.")

# Initialize the LLM (Requires GOOGLE_API_KEY in your .env)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",  # 3 series can use thinking level
    thinking_level = THINKING_LEVEL,
    api_key=GEMINI_API_KEY
)
structured_llm = llm.with_structured_output(TickerResolutionSchema)

def ticker_resolution_node(state: FinancialState) -> Dict[str, Any]:
    user_query = state.get("user_query", "")
    print(f"\n⚡ [Node: Ticker Resolver] Resolving query: '{user_query}'...")
    
    prompt = f"""
    You are a financial data assistant. The user wants to pull financial data for the following query:
    "{user_query}"
    
    Determine the exact, valid Yahoo Finance ticker symbol for this query.
    If it's an international stock, ensure the correct suffix is appended (e.g., .KL for Malaysia, .L for London, etc.).
    If the user query is already a valid ticker, simply format it to uppercase and return it.
    """
    
    try:
        response = structured_llm.invoke(prompt)
        resolved_ticker = response.ticker.upper()
        print(f"✅ [Node: Ticker Resolver] Resolved to ticker: {resolved_ticker}")
        return {"ticker": resolved_ticker}
    except Exception as e:
        print(f"❌ [Node: Ticker Resolver] Failed to resolve ticker: {str(e)}")
        # Fallback to just using the raw query if resolution fails
        return {"ticker": user_query.upper()}
