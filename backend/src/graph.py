# LangGraph node compilation and routing logic

# backend/src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import FinancialState
from src.agents.resolution import ticker_resolution_node
from src.agents.sentiment import news_research_node
from src.agents.fundamental import fundamental_analyst_node
from src.agents.risk import risk_auditor_node       # Import new node
from src.agents.synthesis import synthesis_analyst_node

workflow = StateGraph(FinancialState)

# 1. Register all 5 nodes
workflow.add_node("ticker_resolver", ticker_resolution_node)
workflow.add_node("news_researcher", news_research_node)
workflow.add_node("fundamental_analyst", fundamental_analyst_node)
workflow.add_node("risk_auditor", risk_auditor_node) # Add node
workflow.add_node("synthesis_analyst", synthesis_analyst_node)

# 2. Re-wire edges to inject the Risk Auditor ahead of final Synthesis
workflow.add_edge(START, "ticker_resolver")
workflow.add_edge("ticker_resolver", "news_researcher")
workflow.add_edge("news_researcher", "fundamental_analyst")
workflow.add_edge("fundamental_analyst", "risk_auditor")     # Route to Risk
workflow.add_edge("risk_auditor", "synthesis_analyst")       # Route Risk to Synthesis
workflow.add_edge("synthesis_analyst", END)

fin_sentinel_engine = workflow.compile()
print("⚙️  [Engine] LangGraph updated to a 5-Agent Pipeline containing Ticker Resolution and local Vector RAG.")