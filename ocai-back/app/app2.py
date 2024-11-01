from fastapi import FastAPI, HTTPException
from database import engine, Base
from typing import Dict, Any
from pymilvus import Collection, connections, utility
from ai.indexer.indexer import index_data
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Initialize FastAPI app
app = FastAPI()

# Connect to Milvus
connections.connect(
    host=os.getenv('VDB_HOST'),
    port=os.getenv('VDB_PORT'),
    db_name=os.getenv('VDB_NAME'),
    token=os.getenv('VDB_TOKEN')
)

def search_similar_content(collection_name: str, query_embedding: list, limit: int = 5) -> list:
    """Search for similar content in Milvus collection."""
    try:
        collection = Collection(collection_name)
        collection.load()
        
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        
        results = collection.search(
            data=[query_embedding],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            output_fields=["text"]
        )
        
        return [hit.entity.get('text') for hit in results[0]]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/query")
async def query_rag(query: Dict[Any, Any]):
    """
    RAG endpoint that takes a query, retrieves relevant context, and generates a response.
    """
    try:
        # Generate embedding for the query
        query_embedding = index_data(query["text"])
        
        # Search for similar content
        similar_content = search_similar_content("details_collection2", query_embedding)
        
        # Combine context with query for Gemini
        context = "\n".join(similar_content)
        prompt = f"""Context: {context}\n\nQuestion: {query["text"]}\n\nPlease provide a detailed answer based on the context provided."""
        
        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        return {
            "response": response.text,
            "sources": similar_content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return {"status": "healthy"}