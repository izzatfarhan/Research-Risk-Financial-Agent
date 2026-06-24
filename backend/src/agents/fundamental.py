# Financial data fetching agent
# backend/src/agents/fundamental.py
from typing import Dict, Any
import yfinance as yf
from src.state import FinancialState

def fundamental_analyst_node(state: FinancialState) -> Dict[str, Any]:
    ticker = state["ticker"]
    print(f"\n⚡ [Node: Fundamental Analysis] Fetching live metrics for {ticker}...")
    
    try:
        # Connect to Yahoo Finance for the target stock
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Pull real, live corporate metrics safely using .get() to prevent crashes
        live_metrics = {
            "trailing_PE": round(info.get("trailingPE", 0.0), 2) if info.get("trailingPE") else "N/A",
            "forward_PE": round(info.get("forwardPE", 0.0), 2) if info.get("forwardPE") else "N/A",
            "debt_to_equity": round(info.get("debtToEquity", 0.0) / 100, 2) if info.get("debtToEquity") else "N/A", # yfinance returns D/E as a percentage string sometimes
            "revenue_growth_yoy": f"{round(info.get('revenueGrowth', 0.0) * 100, 2)}%" if info.get("revenueGrowth") else "N/A",
            "free_cash_flow": info.get("freeCashflow", "N/A"),
            "company_name": info.get("longName", "Unknown Company")
        }
        
        print(f"✅ [Node: Fundamental Analysis] Real metrics extracted for {ticker}:")
        print(f"   📊 P/E Ratio: {live_metrics['trailing_PE']} | YoY Rev Growth: {live_metrics['revenue_growth_yoy']}")
        
        return {"extracted_metrics": live_metrics}
        
    except Exception as e:
        print(f"❌ [Node: Fundamental Analysis] Failed to query live data: {str(e)}")
        # Graceful fallback state mutation
        return {
            "extracted_metrics": {
                "trailing_PE": "N/A", 
                "forward_PE": "N/A", 
                "debt_to_equity": "N/A", 
                "revenue_growth_yoy": "N/A",
                "free_cash_flow": "N/A",
                "company_name": "N/A"
            }
        }