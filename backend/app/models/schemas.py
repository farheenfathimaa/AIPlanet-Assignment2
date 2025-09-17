from pydantic import BaseModel
from typing import Optional, Dict

class QuestionRequest(BaseModel):
    question: str

class SolutionResponse(BaseModel):
    question: str
    solution: str
    source: str
    is_correct: Optional[bool] = None

class FeedbackRequest(BaseModel):
    question: str
    solution: str
    rating: int  # e.g., 1 to 5
    comments: Optional[str] = None

class FeedbackResponse(BaseModel):
    message: str