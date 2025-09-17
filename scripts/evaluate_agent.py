# This script would analyze the feedback_data.json to provide metrics on agent performance.
import json
from pathlib import Path

def evaluate_performance():
    """Analyzes feedback data to evaluate agent performance."""
    feedback_file = Path("backend/data/feedback_data.json")
    if not feedback_file.exists():
        print("No feedback data available to evaluate.")
        return

    with open(feedback_file, "r") as f:
        data = json.load(f)
    
    feedback_entries = data.get("feedback_entries", [])
    if not feedback_entries:
        print("No feedback entries found.")
        return

    total_ratings = len(feedback_entries)
    sum_of_ratings = sum(entry.get("rating", 0) for entry in feedback_entries)
    avg_rating = sum_of_ratings / total_ratings
    
    print(f"Agent Performance Evaluation:")
    print(f"Total Feedback Entries: {total_ratings}")
    print(f"Average Rating (1-5): {avg_rating:.2f}")

if __name__ == "__main__":
    evaluate_performance()