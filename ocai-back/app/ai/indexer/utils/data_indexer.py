# Just run this if you deleted the data from knowledge_base!

import formatter
from pymilvus import Collection, connections, utility, FieldSchema, DataType, CollectionSchema
from pathlib import Path
from typing import List
import os
import asyncio
import pickle
import google.generativeai as genai

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
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

# Response generation function
async def generate_response(query_text: str, retrieved_texts: List[str]) -> str:
    # Combine retrieved texts as context
    context = "\n".join(retrieved_texts)
    print(f"Context: {context}")
    # Use the generative AI model to generate a response
    try: 
        response = model.generate_content(f"Context:\n{context}\n\nQuestion:\n{query_text}\n\nAnswer:")
        return response.candidates[0].content.parts
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, but I couldn't generate a response at this time."

# Main function
async def main():
    # Define the collection schema
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=768),
        FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=65535)
    ]

    # Configure the generative AI client (fix typo in env var name)
    api_key = os.getenv("GEMINI_API_KEY")  # Changed from GEMMINI_API_KEY
    genai.configure(api_key=api_key)

    pricing_file = "D:/Personal/Practicas/MADHACKS/OCAI/ocai-back/app/ai/indexer/utils/info/oci_pricing.json"
    details_file = "D:/Personal/Practicas/MADHACKS/OCAI/ocai-back/app/ai/indexer/utils/info/oci_details.json"

    # Formatear los datos
    pricing_text_data = formatter.formatter('pricing', pricing_file)
    details_text_data = formatter.formatter('details', details_file)

    # Combine data if necessary
    all_text_data = pricing_text_data + details_text_data

    # Generate embeddings
    embeddings_pickle_path = Path("./all_data_embeddings.pkl")
    if embeddings_pickle_path.exists():
        with open(embeddings_pickle_path, "rb") as f:
            all_data_embeddings = pickle.load(f)
    else:
        all_data_embeddings = await generate_all_embeddings(all_text_data)
        with open(embeddings_pickle_path, "wb") as f:
            pickle.dump(all_data_embeddings, f)

    # Insert into Milvus
    await add_to_milvus("knowledge_base", all_data_embeddings, all_text_data, fields)

    # Example query
    query_text = "What are the pricing options for OCI compute instances?"

    # Search for relevant documents
    retrieved_texts = await search_in_milvus("knowledge_base", query_text)

    if not retrieved_texts:
        print("No relevant documents found.")
        return

    # Generate response using retrieved documents
    answer = await generate_response(query_text, retrieved_texts)

    print("Generated Answer:")
    print(answer)

if __name__ == "__main__": 
    asyncio.run(main())
