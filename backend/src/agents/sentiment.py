# News & Hugging Face sentiment agent

# backend/src/agents/sentiment.py
import ast
from typing import Dict, Any
from langchain_tavily import TavilySearch
from transformers import pipeline
from src.state import FinancialState

# Initialize tools
search_tool = TavilySearch(max_results=3)

print("⏳ [Engine] Loading local Hugging Face FinBERT model pipeline...")
# This downloads/loads the model locally. It will cache it so future loads take <1 second.
sentiment_pipeline = pipeline("text-classification", model="ProsusAI/finbert")
print("🔥 [Engine] FinBERT pipeline successfully mounted.")

def news_research_node(state: FinancialState) -> Dict[str, Any]:
    ticker = state["ticker"]
    print(f"\n⚡ [Node: News Research] Gathering and scoring sentiment for {ticker}...")
    
    query = f"latest financial performance, stock news, and market sentiment for {ticker}"
    
    try:
        search_results = search_tool.invoke({"query": query})
        
        # 1. Parse out raw content text blocks from the Tavily search dictionary
        text_snippets = []
        if isinstance(search_results, dict) and 'results' in search_results:
            for item in search_results['results']:
                if 'content' in item:
                    text_snippets.append(item['content'])
        else:
            # Fallback if structure behaves like a string representation of a dict
            try:
                parsed_dict = ast.literal_eval(str(search_results))
                text_snippets = [r['content'] for r in parsed_dict.get('results', []) if 'content' in r]
            except Exception:
                text_snippets = [str(search_results)]

        # If zero records are retrieved, gracefully return neutral
        if not text_snippets:
            return {"raw_news": ["No data found"], "sentiment_metrics": {"positive": 0.0, "negative": 0.0, "neutral": 1.0}}

        # 2. Feed text snippets into our local Hugging Face model
        print(f"🧠 [HF Model] Analyzing {len(text_snippets)} financial text blocks...")
        # Add top_k=None to get the full probability distribution for each snippet
        hf_outputs = sentiment_pipeline(text_snippets, top_k=None)
        
        # 3. Calculate average scores to pass to the next agent node
        scores = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        
        # hf_outputs is now a list of lists of dicts
        for snippet_outputs in hf_outputs:
            for output in snippet_outputs:
                label = output['label'].lower()  # 'positive', 'negative', 'neutral'
                score = output['score']          # Confidence weight (0.0 to 1.0)
                scores[label] += score
            
        # Average the values
        total_items = len(text_snippets)
        averaged_scores = {k: round(v / total_items, 3) for k, v in scores.items()}
        print(f"📊 [HF Model] Derived Sentiment Weights: {averaged_scores}")

        return {
            "raw_news": text_snippets,
            "sentiment_metrics": averaged_scores
        }
        
    except Exception as e:
        print(f"❌ [Node: News Research] Node orchestration failed: {str(e)}")
        return {
            "raw_news": [f"Error processing context for {ticker}."],
            "sentiment_metrics": {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
        }