import dotenv
import os
import google.generativeai as genai
from .utils import formatter
from pymilvus import Collection, connections, utility

# Load environment variables
dotenv.load_dotenv()

# Fetch the API key from environment
api_key = os.getenv('GEMINI_API_KEY')

# Authenticate with the API key
genai.configure(api_key=api_key)

# Load and format pricing and details data
formatted_pricing_data = formatter.formatter('pricing', 'ocai-back\app\ai\indexer\utils\info\oci_details.json')
formatted_details_data = formatter.formatter('details', 'ocai-back\app\ai\indexer\utils\info\oci_pricing.json')

def index_data(data):
    # Use the 'embed_content' method for embeddings
    response = genai.embed_content(
        model="models/text-embedding-004", 
        content=data,
        task_type="RETRIEVAL_DOCUMENT"  # Adjust task type if needed
    )
    
    # Return the embedding vector
    return response['embedding']

def add_to_milvus(collection_name, data):
    # Connect to Milvus
    connections.connect(host=os.getenv('VDB_HOST'), port=os.getenv('VDB_PORT'), db_name=os.getenv('VDB_NAME'), token=os.getenv('VDB_TOKEN'))
    
    # Create a collection if it doesn't exist
    if not Collection.exists(collection_name):
        collection = Collection(name=collection_name, schema=your_schema)  # Define your schema
    else:
        collection = Collection(name=collection_name)
    
    # Iterate over the data and add embeddings to Milvus
    for item in data:
        embedding = index_data(item)
        # Insert the embedding into the collection
        collection.insert([embedding])

# Example usage
add_to_milvus('pricing_collection', formatted_pricing_data)
add_to_milvus('details_collection', formatted_details_data)
