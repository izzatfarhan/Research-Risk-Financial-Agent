# backend/run.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

from src.graph import fin_sentinel_engine

def run_test():
    print("🚀 Initializing FinSentinel Local Test Run...")
    
    # Mocking user input
    initial_input = {
        "ticker": "NVDA",
        "raw_news": [],
        "extracted_metrics": {},
        "final_memo": {}
    }
    
    # Invoke the engine
    final_output = fin_sentinel_engine.invoke(initial_input)
    
    print("\n================ TEST COMPLETED ================")
    print(f"Ticker Processed: {final_output['ticker']}")
    print(f"Raw News Captured Count: {len(final_output['raw_news'])}")
    print("Sample Data extracted:\n", final_output['raw_news'][0][:300] + "...")
    print("================================================")

if __name__ == "__main__":
    run_test()