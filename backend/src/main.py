# backend/src/main.py
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Ensure environment variables load for the server instance
backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=backend_dir / ".env")

# Import your compiled LangGraph engine
from src.graph import fin_sentinel_engine

app = FastAPI(
    title="FinSentinel AI Engine API",
    description="Production-grade API wrapper for multi-agent financial analytics",
    version="0.1.0"
)

# Enable CORS so your future Next.js app (running on port 3000) can securely connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request payload structure using Pydantic
class TickerRequest(BaseModel):
    ticker: str

@app.get("/")
def read_root():
    return {"status": "healthy", "engine": "FinSentinel LangGraph Multi-Agent Active"}

@app.post("/api/analyze")
async def analyze_ticker(payload: TickerRequest):
    ticker_upper = payload.ticker.upper().strip()
    if not ticker_upper:
        raise HTTPException(status_code=400, detail="Ticker symbol cannot be empty")
        
    print(f"\n📥 [API] Received analysis request for ticker: {ticker_upper}")
    
    # Initialize the base state to feed into the graph
    initial_state = {  
        "user_query": ticker_upper,
        "ticker": ticker_upper,
        "raw_news": [],
        "extracted_metrics": {},
        "sentiment_metrics": {"positive": 0.0, "negative": 0.0, "neutral": 0.0}, # Init structure
        "final_memo": {}
    }
    
    try:
        final_state = fin_sentinel_engine.invoke(initial_state)
        return {
            "success": True,
            "ticker": final_state["ticker"],
            "sentiment_metrics": final_state["sentiment_metrics"],
            "fundamental_metrics": final_state["extracted_metrics"],
            "investment_memo": final_state["final_memo"]  # New block added
        }
    except Exception as e:
        print(f"❌ [API Error] Graph execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Graph Execution Error: {str(e)}")