# Math Routing Agent

This project is an **Agentic-RAG architecture system with a human-in-the-loop feedback mechanism**, designed to act as a mathematical professor. It intelligently routes user questions to an internal knowledge base or performs a web search to provide accurate, step-by-step solutions.

## Features

* **Intelligent Routing:** Efficiently routes questions to the most appropriate source (Knowledge Base or Web Search).
* **Guardrails:** Includes robust input and output guardrails for safety and relevance.
* **Knowledge Base (RAG):** Uses a Qdrant vector database for fast and relevant information retrieval.
* **Web Search:** Integrates with the Model Context Protocol (MCP) and third-party APIs like Tavily for out-of-domain questions.
* **Human-in-the-Loop:** Incorporates a feedback system powered by DSPy to continuously improve the agent's performance based on user ratings.
* **Full-Stack Application:** Built with a FastAPI backend and a React frontend.

## Project Directory Structure

## Setup Instructions

1.  Clone the repository: `git clone <repository_url>`
2.  Navigate to the project root: `cd math-routing-agent`
3.  Create a virtual environment: `python -m venv venv`
4.  Activate the environment:
      * `source venv/bin/activate` (Linux/Mac)
      * `venv\Scripts\activate` (Windows)
5.  Install backend dependencies: `pip install -r backend/requirements.txt`
6.  Install frontend dependencies: `cd frontend && npm install`
7.  Copy `.env.example` to `.env` in the `backend` directory and fill in your API keys:
    ```
    GOOGLE_API_KEY="your_openai_api_key_here"
    TAVILY_API_KEY="your_tavily_api_key_here"
    ```
8.  Run a Qdrant Docker container: `docker run -p 6333:6333 qdrant/qdrant`
9.  Run the setup script to populate the knowledge base: `python scripts/setup_knowledge_base.py`
10. Start the backend server: `cd backend && python run.py`
11. Start the frontend development server: `cd frontend && npm start`

The application will be accessible at `http://localhost:3000`.

## Demo Video

[Link](https://drive.google.com/file/d/1B9R8HA0IHD5IHNY8sxHyCusXvXuam5Jn/view?usp=sharing)

## Source Code

[Link](https://github.com/farheenfathimaa/Math-Routing-Agent.git)
