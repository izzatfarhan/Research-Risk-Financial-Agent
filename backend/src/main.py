from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph import fin_sentinel_app  # Your LangGraph instance

app = FastAPI()

# Allow Next.js to talk to FastAPI locally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TickerRequest(BaseModel):
    ticker: str

@app.post("/api/analyze")
async def analyze_ticker(req: TickerRequest):
    # Invoke your LangGraph state machine!
    initial_state = {"ticker": req.ticker, "raw_news": [], "financial_metrics": {}, "risk_analysis": [], "final_memo": {}}
    result = fin_sentinel_app.invoke(initial_state)
    return result