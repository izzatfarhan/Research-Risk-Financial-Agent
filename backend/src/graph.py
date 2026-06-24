# LangGraph node compilation and routing logic

# backend/src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import FinancialState
from src.agents.sentiment import news_research_node
from src.agents.fundamental import fundamental_analyst_node
from src.agents.synthesis import synthesis_analyst_node  # New Import
from src.agents.resolution import ticker_resolution_node

# 1. Initialize the workflow builder
workflow = StateGraph(FinancialState)

# 2. Add all nodes to the network
workflow.add_node("ticker_resolver", ticker_resolution_node)
workflow.add_node("news_researcher", news_research_node)
workflow.add_node("fundamental_analyst", fundamental_analyst_node)
workflow.add_node("synthesis_analyst", synthesis_analyst_node) # Add node

# 3. Establish the execution path
workflow.add_edge(START, "ticker_resolver")
workflow.add_edge("ticker_resolver", "news_researcher")
workflow.add_edge("news_researcher", "fundamental_analyst")
workflow.add_edge("fundamental_analyst", "synthesis_analyst") # Route Node 2 to Node 3
workflow.add_edge("synthesis_analyst", END)                  # Route Node 3 to End

# 4. Compile into a runnable application
fin_sentinel_engine = workflow.compile()
print("⚙️  [Engine] LangGraph State Machine updated to a 4-Agent Pipeline.")