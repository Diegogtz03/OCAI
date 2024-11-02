import requests
import json

def test_rag_query():
    url = "http://localhost:8000/query"
    
    # Test queries
    test_queries = [
        "What is Oracle Cloud Infrastructure?",
        "How does OCI pricing work?",
        "What are the different types of compute instances?",
    ]
    
    for query in test_queries:
        payload = {"text": query}
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            result = response.json()
            print("\n" + "="*50)
            print(f"Query: {query}")
            print("\nResponse:", result["response"])
            print("\nSources:")
            for idx, source in enumerate(result["sources"], 1):
                print(f"\n{idx}. {source[:200]}...")  # Print first 200 chars of each source
                
        except requests.exceptions.RequestException as e:
            print(f"Error querying RAG: {e}")
            
if __name__ == "__main__":
    test_rag_query() 