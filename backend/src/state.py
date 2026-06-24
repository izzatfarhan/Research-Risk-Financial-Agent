# The Pydantic and TypedDict graph schemas

# backend/src/state.py
from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field

# This is the strict JSON schema we want our final output to conform to
class InvestmentMemo(BaseModel):
    ticker: str = Field(description="The stock ticker symbol")
    company_name: str = Field(description="Full company name")
    market_sentiment: str = Field(description="Summary of current news sentiment")
    key_metrics: Dict[str, Any] = Field(description="Financial metrics like P/E ratio, revenue growth")
    investment_thesis: str = Field(description="Final buy/sell/hold justification")

# This is the state passed between nodes in LangGraph
class FinancialState(TypedDict):
    ticker: str
    raw_news: List[str]
    extracted_metrics: Dict[str, Any]
    sentiment_metrics: Dict[str, float]  # New: To store averaged scores like {"positive": 0.7, "negative": 0.1, ...}
    final_memo: Dict[str, Any]