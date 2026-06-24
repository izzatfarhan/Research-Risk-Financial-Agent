# LangGraph node compilation and routing logic

# backend/src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import FinancialState
from src.agents.sentiment import news_research_node

# 1. Initialize the workflow builder with our schema
workflow = StateGraph(FinancialState)

# 2. Add our node to the graph network
workflow.add_node("news_researcher", news_research_node)

# 3. Establish the execution lines (Wiring)
workflow.add_edge(START, "news_researcher")
workflow.add_edge("news_researcher", END)

# 4. Compile into a runnable application
fin_sentinel_engine = workflow.compile()
print("⚙️  [Engine] LangGraph State Machine compiled successfully.")