from fastapi import FastAPI, HTTPException
from database import engine, Base
from typing import Dict, Any
from ai.indexer.indexer import (
    generate_embedding,
    search_in_milvus,
    connect_milvus,
    add_to_milvus
)
from services.gemini_service import GeminiService
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pymilvus import Collection, utility, FieldSchema, DataType

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Initialize services
gemini_service = GeminiService()

# Connect to Milvus
connect_milvus()

# Define collection fields
fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=65535)
]

@app.get("/collections")
async def list_collections():
    """Endpoint to list all collections and show their document count."""
    try:
        collections = utility.list_collections()
        collection_data = []
        for name in collections:
            collection = Collection(name)
            collection.load()
            stats = collection.num_entities
            collection_data.append({
                "collection_name": name,
                "num_entities": stats
            })
        return {"collections": collection_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing collections: {str(e)}")

@app.get("/collection/{collection_name}")
async def get_collection_data(collection_name: str, limit: int = 5):
    """Endpoint to get data from a specific Milvus collection."""
    try:
        results = await search_in_milvus(collection_name, "", limit)
        return {"collection_name": collection_name, "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting collection data: {str(e)}")

class QueryInput(BaseModel):
    text: str

@app.post("/query")
async def query_rag(query: QueryInput):
    """RAG endpoint that takes a query, retrieves relevant context, and generates a response."""
    try:
        # Generate embedding with error handling
        query_embedding = await generate_embedding(query.text)
        if query_embedding is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate embedding for the query text"
            )
        
        # Search in knowledge base
        retrieved_texts = await search_in_milvus("knowledge_base", query.text, top_k=5)
        
        # Format sources
        sources = [{
            "collection": "knowledge_base",
            "content": text,
            "score": 0  # Score information not available in current implementation
        } for text in retrieved_texts]
        
        # Generate response using Gemini
        context = "\n".join(retrieved_texts)
        response = await gemini_service.generate_response(query.text, context)
        
        return {
            "response": response,
            "sources": sources
        }
    except Exception as e:
        print(f"Error in query_rag: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/initialize-collections")
async def initialize_collections():
    """Initialize Milvus collections for OCI data."""
    try:
        # Initialize collections with proper schema
        await add_to_milvus("knowledge_base", [], [], fields)
        return {"status": "Collections initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing collections: {str(e)}")

@app.get("/")
async def read_root():
    return {"status": "healthy"}

@app.get("/health")
async def health_check():
    """Check the health status of the application and its dependencies."""
    try:
        # Check Milvus connection
        collections = utility.list_collections()
        
        # Check if Gemini service is initialized
        if not gemini_service:
            return {
                "status": "unhealthy",
                "details": {
                    "milvus": "ok",
                    "gemini": "not initialized"
                }
            }
            
        return {
            "status": "healthy",
            "details": {
                "milvus": "ok",
                "gemini": "ok",
                "collections": len(collections)
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "details": {
                "error": str(e)
            }
        }
