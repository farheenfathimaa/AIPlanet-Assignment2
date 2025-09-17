import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables as early as possible
load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "math_problems"

    class Config:
        env_file = ".env"

settings = Settings()