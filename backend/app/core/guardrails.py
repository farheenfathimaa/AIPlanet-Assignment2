import re
from typing import List
from pydantic import BaseModel

class ModerationResult(BaseModel):
    is_safe: bool
    reason: str

def is_math_related(text: str) -> bool:
    """A simple check to see if the query contains mathematical terms."""
    math_keywords = ["solve", "equation", "theorem", "calculate", "find", "integral", "derivative", "geometry", "algebra", "probability", "parabola", "function", "graph", "formula", "area", "volume", "history", "concept", "explain", "mathematics"]
    if any(keyword in text.lower() for keyword in math_keywords):
        return True
    return False

def input_guardrail(text: str) -> ModerationResult:
    """Checks input for safety and relevance."""
    if re.search(r"how to build a bomb|kill", text, re.IGNORECASE):
        return ModerationResult(is_safe=False, reason="Detected harmful query.")
    
    # Simple check for math relevance. For a real app, this would be an LLM call.
    if not is_math_related(text):
        return ModerationResult(is_safe=False, reason="Query is not related to mathematics.")
    
    return ModerationResult(is_safe=True, reason="Query is safe and relevant.")

def output_guardrail(text: str) -> ModerationResult:
    """Checks output for safety and appropriateness."""
    if "I cannot provide that information" in text:
        return ModerationResult(is_safe=False, reason="LLM provided a canned, unhelpful response.")

    # More complex checks would go here, e.g., PII detection, or LLM-based fact-checking.
    return ModerationResult(is_safe=True, reason="Response is safe and appropriate.")