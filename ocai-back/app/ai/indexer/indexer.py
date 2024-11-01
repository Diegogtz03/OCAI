import dotenv
import os
import google.generativeai as genai
from typing import List, Dict, Any
from pymilvus import Collection, connections, utility
from .utils import formatter

# Load environment variables and configure
dotenv.load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Define schema for Milvus collections
COLLECTION_SCHEMA = {
    'fields': [
        {'name': 'id', 'dtype': 'INT64', 'is_primary': True, 'auto_id': True},
        {'name': 'embedding', 'dtype': 'FLOAT_VECTOR', 'dim': 768}  # Adjust dimension as needed
    ]
}

def index_data(data: str) -> List[float]:
    """
    Generate embeddings for the given text data.
    
    Args:
        data (str): Text content to be embedded
        
    Returns:
        List[float]: Embedding vector
    """
    try:
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=data,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response['embedding']
    except Exception as e:
        raise Exception(f"Failed to generate embedding: {str(e)}")

def add_to_milvus(collection_name: str, data: List[str]) -> None:
    """
    Add embeddings to Milvus collection.
    
    Args:
        collection_name (str): Name of the Milvus collection
        data (List[str]): List of text data to be embedded and stored
    """
    try:
        # Connect to Milvus
        connections.connect(
            host=os.getenv('VDB_HOST'),
            port=os.getenv('VDB_PORT'),
            db_name=os.getenv('VDB_NAME'),
            token=os.getenv('VDB_TOKEN')
        )

        # Create or get collection
        if not utility.has_collection(collection_name):
            collection = Collection(
                name=collection_name,
                schema=COLLECTION_SCHEMA
            )
        else:
            collection = Collection(name=collection_name)

        # Process and insert data
        embeddings = [index_data(item) for item in data]
        collection.insert([embeddings])
        
    except Exception as e:
        raise Exception(f"Failed to add data to Milvus: {str(e)}")
    finally:
        connections.disconnect()

def main():
    """Initialize the indexing process for pricing and details data."""
    try:
        # Load and format data
        formatted_pricing_data = formatter.formatter(
            'pricing',
            'ocai-back/app/ai/indexer/utils/info/oci_details.json'
        )
        formatted_details_data = formatter.formatter(
            'details',
            'ocai-back/app/ai/indexer/utils/info/oci_pricing.json'
        )

        # Index data
        add_to_milvus('pricing_collection', formatted_pricing_data)
        add_to_milvus('details_collection', formatted_details_data)
        
    except Exception as e:
        raise Exception(f"Indexing process failed: {str(e)}")

if __name__ == "__main__":
    main()
