# backend/src/agents/risk.py
from typing import Dict, Any
from src.tools.vector_store import get_vector_store_retriever
from src.state import FinancialState

def risk_auditor_node(state: FinancialState) -> Dict[str, Any]:
    ticker = state["ticker"]
    print(f"\n⚡ [Node: Risk Auditor] Querying internal database records for {ticker} liabilities...")
    
    try:
        retriever = get_vector_store_retriever()
        query = f"{ticker} potential litigation, supply chain bottlenecks, regulatory risks, environmental penalties"
        
        # Query local vector store
        relevant_docs = retriever.invoke(query)
        
        # Merge retrieved context fragments together
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
        if not context_text:
            context_text = "No internal historical compliance dossiers or supplementary documents indexed for this asset."
            
        print(f"✅ [Node: Risk Auditor] Internal risk context compiled ({len(relevant_docs)} source blocks found).")
        return {"risk_analysis": [context_text]}
        
    except Exception as e:
        print(f"❌ [Node: Risk Auditor] Vector query step faulted: {str(e)}")
        return {"risk_analysis": [f"Error checking local vector datastores: {str(e)}"]}