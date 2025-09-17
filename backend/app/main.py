from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router as api_router

app = FastAPI(
    title="Math Routing Agent",
    description="An Agentic-RAG system that acts as a mathematical professor."
)

# CORS middleware for frontend communication
origins = ["http://localhost:3000"]  # React default port
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Math Routing Agent API!"}