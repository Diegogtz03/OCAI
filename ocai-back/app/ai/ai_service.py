from typing import Dict, Any, List
from ai.indexer.indexer import (
    generate_embedding,
    search_in_milvus,
    connect_milvus,
    add_to_milvus
)
from services.gemini_service import GeminiService
from pymilvus import Collection, utility, FieldSchema, DataType

class AIService:
    def __init__(self):
        self.gemini_service = GeminiService()
        self.fields = [
            FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=768),
            FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=65535)
        ]
        connect_milvus()

    async def list_collections(self) -> Dict[str, List[Dict[str, Any]]]:
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

    async def get_collection_data(self, collection_name: str, limit: int = 5) -> Dict[str, Any]:
        results = await search_in_milvus(collection_name, "", limit)
        return {"collection_name": collection_name, "data": results}

    async def query_rag(self, query_text: str) -> Dict[str, Any]:
        # Generate embedding
        query_embedding = await generate_embedding(query_text)
        if query_embedding is None:
            raise ValueError("Failed to generate embedding for the query text")
        
        # Search in knowledge base
        retrieved_texts = await search_in_milvus("knowledge_base", query_text, top_k=5)
        
        # Format sources
        sources = [{
            "collection": "knowledge_base",
            "content": text,
            "score": 0
        } for text in retrieved_texts]
        
        # Generate response using Gemini
        context = "\n".join(retrieved_texts)
        response = await self.gemini_service.generate_response(query_text, context)
        
        return {
            "response": response,
            "sources": sources
        }

    async def initialize_collections(self) -> Dict[str, str]:
        await add_to_milvus("knowledge_base", [], [], self.fields)
        return {"status": "Collections initialized successfully"}

    async def health_check(self) -> Dict[str, Any]:
        # Check Milvus connection
        collections = utility.list_collections()
        
        # Check if Gemini service is initialized
        if not self.gemini_service:
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