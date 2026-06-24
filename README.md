# The Project: "FinSentinel" — Multi-Agent Financial Research & Risk Assessment Engine
Instead of a basic "Chat with your financial PDF" app, you will build an Autonomous Multi-Agent Workflow that analyzes a company's financial health, evaluates market sentiment, maps supply-chain risks, and outputs a structured Investment Memo.

## User Journey

### Input
A user runs this locally hosted backend (via your Next.js UI) and enters a stock ticker symbol, e.g., `NVDA`.

### The FinSentinel Workflow (Autonomous Multi-Agent System)

Instead of fetching a single PDF, the backend spins up a team of agents that collaborate to analyze the company:

1. **The Financial Analyst Agent** (Data Acquisition)
   - *Task*: Fetches historical financial data for the ticker using yfinance (P/E ratio, revenue growth, debt-to-equity, EBITDA).
   - *Output*: A structured dictionary of key financial metrics.

2. **The News Aggregator & Sentiment Agent** (Qualitative Context)
   - *Task*: Scans recent financial news headlines using a local LLM (like Phi-3) or an API to gauge market sentiment (Positive/Negative/Neutral).
   - *Output*: Sentiment score and a list of "Risk/Opportunity" keywords.

3. **The Supply Chain Analyst Agent** (Risk Intelligence)
   - *Task*: **This is the advanced part**. It analyzes the company's primary suppliers and competitors (extracted from the financial data) to identify geographical or geopolitical risks (e.g., "High dependence on Taiwan for chips").
   - *Output*: Supply chain risks and geographic vulnerabilities.

4. **The Executive Report Generator Agent** (Final Synthesis)
   - *Task*: Compiles all outputs into a single, structured Investment Memo.

### The Output (Investment Memo)
```json
{
    "ticker": "NVDA",
    "financial_health": "Strong revenue growth, but high P/E ratio suggests overvaluation.",
    "sentiment": "Positive (78%)",
    "supply_chain_risks": ["Geographic concentration in Taiwan"],
    "final_verdict": "Proceed with caution. Strong fundamentals, but high valuation and geopolitical risk."
}
```

## Technical Architecture
- **Backend**: Python FastAPI + LangGraph (or CrewAI).
- **Graph Logic**: Uses a **Conditional Edge** (i.e., a router) to decide which agent runs next based on the data from the previous agent.
- **Data Flow**: Custom State (Pydantic) to pass JSON objects between agents.
- **LLM**: Local model (Ollama/Phi-3) for privacy and cost savings.


## FinSentinel System Architecture

            [ User Input Ticker ]
                        │
                        ▼
             ┌─────────────────────┐
             │  Supervisor Agent   │◀───────────────────────|
             └─────────────────────┘                         │
              /        │          \                          │
             ▼         ▼           ▼                         │
   ┌───────────┐ ┌───────────┐ ┌───────────┐                 │
   │ FundaBot  │ │ VisionBot │ │ EchoBot   │                 │
   │ (Earnings │ │ (Charts   │ │ (Realtime │                 │
   │  & SEC)   │ │ &Technical)│ News Semantics)             │
   └───────────┘ └───────────┘ └───────────┘                 │
             \         │          /                          │
              ▼        ▼         ▼                           │
             ┌─────────────────────┐                         │
             │   Synthesis Node    │                         │
             └─────────────────────┘                         │
                        │                                    │
                        ▼                                    │
             ┌─────────────────────┐  No (Refine)            │
             │ Human-in-the-Loop   ├─────────────────────────┘
             │      Approve?       │
             └─────────────────────┘
                        │ Yes
                        ▼
               [ Generated Memo ]