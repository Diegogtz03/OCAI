from fastapi import FastAPI, HTTPException
from database import engine, Base
from typing import Dict, Any
from pydantic import BaseModel
from ai.ai_service import AIService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Initialize AI Service
ai_service = AIService()

class QueryInput(BaseModel):
    text: str

@app.get("/collections")
async def list_collections():
    """Endpoint to list all collections and show their document count."""
    try:
        return await ai_service.list_collections()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing collections: {str(e)}")

@app.get("/collection/{collection_name}")
async def get_collection_data(collection_name: str, limit: int = 5):
    """Endpoint to get data from a specific Milvus collection."""
    try:
        return await ai_service.get_collection_data(collection_name, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting collection data: {str(e)}")

@app.post("/query")
async def query_rag(query: QueryInput):
    """RAG endpoint that takes a query, retrieves relevant context, and generates a response."""
    try:
        return await ai_service.query_rag(query.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/initialize-collections")
async def initialize_collections():
    """Initialize Milvus collections for OCI data."""
    try:
        return await ai_service.initialize_collections()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing collections: {str(e)}")

@app.get("/")
async def read_root():
    return {"status": "healthy"}

@app.get("/health")
async def health_check():
    """Check the health status of the application and its dependencies."""
    try:
        return await ai_service.health_check()
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": {
                "error": str(e)
            }
        }