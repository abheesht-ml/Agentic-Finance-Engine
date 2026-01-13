from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.graph import build_graph 

app = FastAPI(
    title="Financial RAG Agent",
    description="A High-Performance API for analyzing 10-K financial reports.",
    version="1.0"
)

class ChatRequest(BaseModel):
    query: str

agent_app = build_graph()

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        user_input = payload.query
        print(f"Received: {user_input}")

        inputs = {"messages": [HumanMessage(content=user_input)]}
        result = agent_app.invoke(inputs)
        
        final_answer = result["messages"][-1].content
        
        return {
            "status": "success",
            "answer": final_answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from src.ingestion import fetch_10k, html_to_hybrid
from src.database import indexed_document
from src.input_schemas import InputfromUser

class IngestRequest(BaseModel):
    ticker: str
    year: int = 1

@app.post("/ingest")
async def ingest_endpoint(payload: IngestRequest):
    try:
        config = InputfromUser(company_ticker=payload.ticker, years=payload.year)
        
        # 1. Fetch
        print(f"Fetching 10-K for {payload.ticker}...")
        html_path = fetch_10k(config)
        
        # 2. Convert
        print(f"Converting HTML to Hybrid format...")
        processed_doc = html_to_hybrid(html_path, config)
        
        # 3. Index
        print(f"Indexing into Vector Store...")
        indexed_document(processed_doc)
        
        return {
            "status": "success", 
            "message": f"Successfully ingested 10-K for {payload.ticker}",
            "ticker": payload.ticker
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Financial Agent is ready."}