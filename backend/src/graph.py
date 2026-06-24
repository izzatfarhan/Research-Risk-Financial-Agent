# LangGraph node compilation and routing logic

# backend/src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import FinancialState
from src.agents.sentiment import news_research_node
from src.agents.fundamental import fundamental_analyst_node  # Import new node

# 1. Initialize the workflow builder
workflow = StateGraph(FinancialState)

# 2. Add BOTH nodes to the graph network
workflow.add_node("news_researcher", news_research_node)
workflow.add_node("fundamental_analyst", fundamental_analyst_node)

# 3. Establish the sequential execution path
workflow.add_edge(START, "news_researcher")
workflow.add_edge("news_researcher", "fundamental_analyst") # Route Node 1 to Node 2
workflow.add_edge("fundamental_analyst", END)               # Route Node 2 to End

# 4. Compile into a runnable application
fin_sentinel_engine = workflow.compile()
print("⚙️  [Engine] LangGraph State Machine updated to multi-agent sequential pipeline.")