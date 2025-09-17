import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None  # Use Optional[str]
    GOOGLE_API_KEY: Optional[str] = None  # Also make this optional to prevent errors
    TAVILY_API_KEY: str
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "math_problems"

    class Config:
        env_file = ".env"

settings = Settings()