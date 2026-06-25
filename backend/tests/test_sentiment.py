import os
from dotenv import load_dotenv
load_dotenv()

from src.agents.sentiment import news_research_node

state = {"ticker": "AAPL"}
try:
    result = news_research_node(state)
    print("RESULT:")
    print(result)
except Exception as e:
    print(f"Exception: {e}")
