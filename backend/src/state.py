# The Pydantic and TypedDict graph schemas

# backend/src/state.py
from typing import TypedDict, List, Dict, Any
from pydantic import BaseModel, Field

# This is the strict JSON schema we want our final output to conform to
class InvestmentMemoSchema(BaseModel):
    executive_summary: str = Field(description="A concise 2-3 sentence overview of the company's current position.")
    sentiment_analysis: str = Field(description="Interpretation of why the market sentiment is skewed based on recent events.")
    fundamental_health: str = Field(description="Evaluation of the valuation ratios and growth metrics.")
    risk_rating: str = Field(description="LOW, MEDIUM, or HIGH risk classification with a brief justification.")

# This is the state passed between nodes in LangGraph
class FinancialState(TypedDict):
    user_query: str
    ticker: str
    raw_news: List[str]
    extracted_metrics: Dict[str, Any]
    sentiment_metrics: Dict[str, float]  # New: To store averaged scores like {"positive": 0.7, "negative": 0.1, ...}
    risk_analysis: List[str]  # New: Ingests text extracted from your PDF via Vector DB
    final_memo: Dict[str, Any]