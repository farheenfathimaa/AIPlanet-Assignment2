import sys
from pathlib import Path

# Add the project's root directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from pathlib import Path
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from backend.app.core.config import settings

DATA_FILE = Path("backend/data/math_dataset.json")
COLLECTION_NAME = settings.QDRANT_COLLECTION

def create_and_populate_knowledge_base():
    """Reads a dataset, creates a collection, and populates Qdrant."""
    client = QdrantClient(url=settings.QDRANT_URL)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    try:
        # Delete existing collection to start fresh
        client.delete_collection(collection_name=COLLECTION_NAME)
    except Exception:
        print(f"Collection '{COLLECTION_NAME}' did not exist. Creating new.")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=model.get_sentence_embedding_dimension(), distance=models.Distance.COSINE),
    )

    with open(DATA_FILE, "r") as f:
        dataset = json.load(f)["problems"]
    
    points = []
    for i, problem in enumerate(dataset):
        problem_text = problem["question"] + " " + problem["solution"]
        vector = model.encode(problem_text).tolist()
        points.append(
            models.PointStruct(
                id=i,
                vector=vector,
                payload={"question": problem["question"], "solution": problem["solution"]}
            )
        )
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        wait=True,
        points=points
    )
    print(f"Successfully populated Qdrant with {len(dataset)} problems.")

if __name__ == "__main__":
    # Create a sample dataset file for demonstration
    sample_data = {
        "problems": [
            {
                "question": "What is the definite integral of sin(x) from 0 to pi?",
                "solution": "The integral of sin(x) is -cos(x). Evaluating from 0 to pi, we get (-cos(pi)) - (-cos(0)) = (-(-1)) - (-(1)) = 1 + 1 = 2."
            },
            {
                "question": "Solve the quadratic equation x^2 - 4x + 4 = 0.",
                "solution": "This is a perfect square trinomial, (x-2)^2 = 0. The only solution is x = 2."
            },
            {
                "question": "A fair coin is flipped 3 times. What is the probability of getting exactly 2 heads?",
                "solution": "Total possible outcomes are 2^3 = 8. The outcomes with exactly 2 heads are HHT, HTH, THH. There are 3 such outcomes. The probability is 3/8."
            }
        ]
    }
    
    if not DATA_FILE.parent.exists():
        DATA_FILE.parent.mkdir(parents=True)
    with open(DATA_FILE, "w") as f:
        json.dump(sample_data, f, indent=4)
        
    create_and_populate_knowledge_base()