from app.ai.indexer.utils import formatter
import google.generativeai as genai
from pymilvus import Collection, connections, utility, FieldSchema, DataType, CollectionSchema
from pathlib import Path
from typing import List
import os
import asyncio
import pickle

async def generate_batch_embeddings(batch_data: List[str]):
    # Let gemini convert text to embedding (numerical representation)
    try:
        response = await genai.embed_content_async(
            model="models/text-embedding-004",
            content=batch_data,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return [response.get("embedding") for res in response]
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return []
    
async def generate_embedding(data: str):
    # Let gemini convert text to embedding (numerical representation)
    try:
        response = await genai.embed_content_async(
            model="models/text-embedding-004",
            content=data,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response.get("embedding")
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
    
async def _generate_all_embeddings(data: List[str], batch_size: int = 10) -> List[List[float]]:
    embeddings = []
    for i in range(0, len(data), batch_size):
        batch_data = data[i: i + batch_size]
        batch_embeddings = await generate_batch_embeddings(batch_data)
        embeddings.extend(batch_embeddings)
    return embeddings

async def generate_all_embeddings(data: List[str]) -> List[List[float]]:
    embeddings = []
    for item in data:
        embedding = await generate_embedding(item)
        if embedding is not None:
            embeddings.append(embedding)
    return embeddings

def connect_milvus():
    return connections.connect(
        host=os.getenv("VDB_HOST"),
        port=os.getenv("VDB_PORT"),
        db_name=os.getenv("VDB_NAME"),
        token=os.getenv("VDB_TOKEN")
    )

async def add_to_milvus(
    collection_name: str,
    embeddings_data: List[List[List[float]]],  
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

    # Loop over each set of embeddings to insert them one by one
    for embeddings in embeddings_data:
        if embeddings:
            # Prepare data list with only the embeddings if IDs are auto-generated
            data = [embeddings]  # Only the embeddings, as the schema has auto_id=True

            # Insert the embeddings into the collection
            try:
                collection.insert(data)
                print(f"Inserted {len(embeddings)} embeddings into '{collection_name}'.")
            except Exception as e:
                print(f"Error inserting embeddings: {e}")
        else:
            print("No embeddings to insert for this dataset.")


async def main():
    fields = [
        FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=768)  # Change dim to 768
    ]


    api_key = os.getenv("GEMMINI_API_KEY")
    genai.configure(api_key=api_key)

    formatted_pricing_data = formatter.formatter('pricing', Path("app/ai/indexer/utils/info/oci_pricing.json"))
    formatted_details_data = formatter.formatter('details', Path("app/ai/indexer/utils/info/oci_details.json"))


    pricing_embeddings_path = Path("./pricing_data_embeddings.pkl")
    details_embeddings_path = Path("./details_data_embeddings.pkl")

    if pricing_embeddings_path.exists():
        with open(pricing_embeddings_path, "rb") as f:
            pricing_data_embeddings = pickle.load(f)
    else:
        pricing_data_embeddings = await generate_all_embeddings(formatted_pricing_data)
        with open(pricing_embeddings_path, "wb") as f:
            pickle.dump(pricing_data_embeddings, f)

    if details_embeddings_path.exists():
        with open(details_embeddings_path, "rb") as f:
            details_data_embeddings = pickle.load(f)
    else:
        details_data_embeddings = await generate_all_embeddings(formatted_details_data)
        with open(details_embeddings_path, "wb") as f:
            pickle.dump(details_data_embeddings, f)

    # await add_to_milvus("pricing_collection2", [pricing_data_embeddings], fields)
    await add_to_milvus("details_collection2", [details_data_embeddings], fields)


if __name__ == "__main__": 
    asyncio.run(main())