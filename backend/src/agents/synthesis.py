# backend/src/agents/synthesis.py
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI 
from src.state import FinancialState, InvestmentMemoSchema
from dotenv import load_dotenv

load_dotenv()
THINKING_LEVEL = "medium"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the LLM (Requires GOOGLE_API_KEY in your .env)
# We set temperature=1.0 because we want analytical, deterministic writing, not creative prose.
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash", temperature=1.0)  
structured_llm = llm.with_structured_output(InvestmentMemoSchema)

def synthesis_analyst_node(state: FinancialState) -> Dict[str, Any]:
    ticker = state["ticker"]
    sentiment = state["sentiment_metrics"]
    metrics = state["extracted_metrics"]
    
    print(f"\n⚡ [Node: Synthesis Analyst] Generating final investment memo for {ticker}...")
    
    # Construct an engineering-grade context prompt
    prompt = f"""
    You are a Senior Portfolio Manager at a quantitative hedge fund. 
    Analyze the following data payload gathered by our automated retrieval agents for ticker symbol: {ticker}.
    
    --- MARKET SENTIMENT DATA (Calculated via local FinBERT) ---
    Positive Sentiment Weight: {sentiment.get('positive')}
    Negative Sentiment Weight: {sentiment.get('negative')}
    Neutral Sentiment Weight: {sentiment.get('neutral')}
    
    --- FINANCIAL FUNDAMENTALS DATA (Live Streamed) ---
    Company Official Name: {metrics.get('company_name')}
    Trailing P/E Ratio: {metrics.get('trailing_PE')}
    Forward P/E Ratio: {metrics.get('forward_PE')}
    Debt to Equity Ratio: {metrics.get('debt_to_equity')}
    YoY Revenue Growth: {metrics.get('revenue_growth_yoy')}
    
    Synthesize these data points into a highly professional Investment Memo. 
    Be objective, critical, and ensure your conclusions logically align with the numerical data provided.
    """
    
    try:
        # Invoke the LLM structured call
        memo_response = structured_llm.invoke(prompt)
        
        print(f"✅ [Node: Synthesis Analyst] Investment Memo structured successfully.")
        # Convert Pydantic model to a clean dictionary to pass back to the state
        return {"final_memo": memo_response.model_dump()}
        
    except Exception as e:
        print(f"❌ [Node: Synthesis Analyst] Synthesis failed: {str(e)}")
        return {
            "final_memo": {
                "executive_summary": "Failed to compile synthesis data.",
                "sentiment_analysis": "N/A",
                "fundamental_health": "N/A",
                "risk_rating": "ERROR"
            }
        }