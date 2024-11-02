# Import necessary libraries
from .utils import formatter
from pymilvus import Collection, connections, utility, FieldSchema, DataType, CollectionSchema
from pathlib import Path
from typing import List
import os
import asyncio
import pickle
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")  # Changed from GEMMINI_API_KEY
genai.configure(api_key=api_key)

if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
genai.configure(api_key=api_key)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 256,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

# Embedding generation functions
async def generate_embedding(data: str):
    try:
        # Use synchronous embed_content instead of async version
        response = genai.embed_content(
            model="models/embedding-001",
            content=data,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

async def generate_all_embeddings(data: List[str]) -> List[List[float]]:
    embeddings = []
    for item in data:
        embedding = await generate_embedding(item)
        if embedding is not None:
            embeddings.append(embedding)
    return embeddings

# Milvus connection and data insertion functions (modified)
def connect_milvus():
    connections.connect(
        alias="default",
        host=os.getenv("VDB_HOST"),
        port=os.getenv("VDB_PORT"),
        db_name=os.getenv("VDB_NAME"),
        token=os.getenv("VDB_TOKEN")
    )

async def add_to_milvus(
    collection_name: str,
    embeddings_data: List[List[float]],
    text_data: List[str],
    fields: List[FieldSchema]
):
    # Connect to Milvus
    connect_milvus()

    # Check if collection exists or create it
    if not utility.has_collection(collection_name):
        schema = CollectionSchema(fields=fields)
        collection = Collection(name=collection_name, schema=schema)
    else:
        collection = Collection(name=collection_name)

    # Prepare data for insertion (modified to match schema)
    data = [
        embeddings_data, # Embeddings
        text_data       # Text data
    ]

    try:
        collection.insert(data)
        print(f"Inserted {len(embeddings_data)} records into '{collection_name}'.")
        # Build index for faster search
        index_params = {
            "metric_type": "L2",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        collection.load()  # Load the collection after creating index
    except Exception as e:
        print(f"Error inserting data: {e}")

# Search function for RAG
async def search_in_milvus(
    collection_name: str,
    query_text: str,
    top_k: int = 5
) -> List[str]:
    # Generate embedding for the query
    query_embedding = await generate_embedding(query_text)

    if query_embedding is None:
        return []

    # Connect to Milvus
    connect_milvus()

    # Load the collection
    collection = Collection(name=collection_name)
    collection.load()

    # Perform the search
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text"]
    )

    # Extract and return the text data from the results
    retrieved_texts = []
    for hits in results:
        for hit in hits:
            retrieved_texts.append(hit.entity.get("text"))

    return retrieved_texts