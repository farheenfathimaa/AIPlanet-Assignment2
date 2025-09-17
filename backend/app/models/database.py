import json
from pathlib import Path
from typing import Dict, Any

FEEDBACK_DATA_FILE = Path("backend/data/feedback_data.json")

def load_feedback_data() -> Dict[str, Any]:
    if not FEEDBACK_DATA_FILE.exists():
        return {"feedback_entries": []}
    with open(FEEDBACK_DATA_FILE, "r") as f:
        return json.load(f)

def save_feedback_entry(entry: Dict[str, Any]):
    data = load_feedback_data()
    data["feedback_entries"].append(entry)
    with open(FEEDBACK_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)