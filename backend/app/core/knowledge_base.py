from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from typing import Tuple, Optional
from .config import settings

client = QdrantClient(url=settings.QDRANT_URL)
model = SentenceTransformer('all-MiniLM-L6-v2')
COLLECTION_NAME = settings.QDRANT_COLLECTION

def create_collection():
    """Creates the Qdrant collection if it does not exist."""
    try:
        client.get_collection(collection_name=COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Creating collection '{COLLECTION_NAME}'...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=model.get_sentence_embedding_dimension(), distance=models.Distance.COSINE),
        )

def search_knowledge_base(query: str) -> Tuple[str, Optional[float]]:
    """Performs a similarity search on the knowledge base."""
    query_vector = model.encode(query).tolist()
    
    try:
        search_result = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=1,
            with_payload=True
        )
        if search_result:
            result = search_result[0]
            if result.score > 0.8:  # Confidence threshold
                return result.payload.get("solution", ""), result.score
    except Exception as e:
        print(f"Error during knowledge base search: {e}")
        return "", None
    
    return "", None