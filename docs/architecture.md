# Math Routing Agent Architecture

## Overview

The Math Routing Agent is a full-stack application designed to be a "mathematical professor." It uses an Agentic-RAG architecture with a human-in-the-loop feedback system.

## High-Level Design



The system is composed of two main components:
1.  **Backend (FastAPI):** Manages the core agentic workflow, API endpoints, database interactions, and integrations with external services.
2.  **Frontend (React):** Provides the user interface for asking questions, viewing solutions, and submitting feedback.

## Key Components and Data Flow

1.  **User Input:** A user asks a math question via the React frontend.
2.  **API Layer (`backend/app/api/routes.py`):**
    * The question is received by the `/api/ask` endpoint.
    * **Input Guardrails:** The query is first checked for safety and relevance. If it fails, an error is returned immediately.
3.  **Math Agent Core (`backend/app/core/math_agent.py`):**
    * A **LangGraph** workflow orchestrates the agent's decisions.
    * **Routing:** The agent decides whether to use the internal Knowledge Base or perform a Web Search. This is a crucial routing step.
4.  **Knowledge Base (`backend/app/core/knowledge_base.py`):**
    * If routed here, the agent queries the **Qdrant vector database**.
    * A **Sentence-Transformer** model is used to create embeddings for semantic search.
    * If a highly similar problem is found, the pre-stored solution is retrieved.
5.  **Web Search (`backend/app/core/web_search.py`):**
    * If no relevant match is found in the knowledge base, the agent uses the **Model Context Protocol (MCP)** to perform a web search via **Tavily**.
    * The search results are extracted and provided as context to the LLM.
6.  **Solution Generation:** The retrieved context (from either the KB or Web Search) is passed to an **LLM (e.g., OpenAI/Anthropic)** to generate the final step-by-step solution.
7.  **Output Guardrails:** The generated solution is checked for safety before being sent back to the frontend.
8.  **Frontend Interface:** The solution is displayed to the user using **MathJax** for proper mathematical rendering.
9.  **Human-in-the-Loop Feedback (`backend/app/core/feedback_system.py`):**
    * The user is prompted to submit feedback on the solution's quality.
    * This feedback is sent to the `/api/feedback` endpoint and stored.
    * This data is used to "self-improve" the agent via a **DSPy**-powered feedback loop, which can re-optimize prompts and model behavior.