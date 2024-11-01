from fastapi import HTTPException
from pymilvus import Collection, connections, utility, DataType, CollectionSchema
import numpy as np
from typing import Dict, Any, List

def convert_numpy_to_native(data):
    """Converts numpy values to native Python types."""
    if isinstance(data, dict):
        return {k: convert_numpy_to_native(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_to_native(i) for i in data]
    elif isinstance(data, (np.float32, np.float64)):
        return float(data)
    elif isinstance(data, (np.int32, np.int64)):
        return int(data)
    return data

def get_collection_stats(collection_name: str) -> Dict[str, Any]:
    """Get statistics for a specific collection."""
    collection = Collection(collection_name)
    collection.load()
    stats = collection.num_entities
    return {
        "collection_name": collection_name,
        "num_entities": convert_numpy_to_native(stats)
    }

def search_similar_content(collection_name: str, query_vector: list, limit: int = 3):
    """
    Busca contenido similar en una colección de Milvus y devuelve resultados formateados.
    """
    try:
        collection = Collection(collection_name)
        collection.load()
        
        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }
        
        results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=limit,
        output_fields=["content", "source"]  # Incluir 'source' en los campos de salida
    )
        
        # Formatear los resultados
        processed_results = []
        for hits in results:
            for hit in hits:
                result_dict = {
                    "score": float(hit.score),  # Convertir a float nativo
                    "content": hit.entity.get('content', ''),
                    "source": hit.entity.get('source', ''),
                }
                processed_results.append(result_dict)
        
        return processed_results
    except Exception as e:
        print(f"Error in search_similar_content: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching in collection: {str(e)}")

def initialize_collection(collection_name: str):
    """Initialize a Milvus collection with the required schema."""
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
    
    dim = 1536  # Dimension of your embeddings
    fields = [
        {"name": "content", "dtype": DataType.VARCHAR, "max_length": 65535},
        {"name": "embedding", "dtype": DataType.FLOAT_VECTOR, "dim": dim},
        {"name": "source", "dtype": DataType.VARCHAR, "max_length": 255}
    ]
    
    schema = CollectionSchema(fields=fields, description=f"Collection for {collection_name}")
    collection = Collection(name=collection_name, schema=schema)
    
    # Create index
    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 1024}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    return collection