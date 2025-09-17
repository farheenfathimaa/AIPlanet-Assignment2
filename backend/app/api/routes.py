from fastapi import APIRouter, HTTPException
from ..models.schemas import QuestionRequest, SolutionResponse, FeedbackRequest, FeedbackResponse
from ..core.guardrails import input_guardrail, output_guardrail
from ..core.math_agent import math_agent, AgentState
from ..models.database import save_feedback_entry
from datetime import datetime

router = APIRouter()

@router.post("/ask", response_model=SolutionResponse)
async def ask_math_question(request: QuestionRequest):
    guardrail_check = input_guardrail(request.question)
    if not guardrail_check.is_safe:
        raise HTTPException(status_code=400, detail=guardrail_check.reason)
    
    try:
        initial_state = AgentState(
            question=request.question,
            retrieved_content="",
            solution="",
            source="error"
        )
        final_state = math_agent.invoke(initial_state)

        output_check = output_guardrail(final_state.get("solution", ""))
        if not output_check.is_safe:
            raise HTTPException(status_code=500, detail="Failed output safety check.")
            
        return SolutionResponse(
            question=final_state.get("question", ""),
            solution=final_state.get("solution", ""),
            source=final_state.get("source", "error")
        )
    except Exception as e:
        # This will print the error to your terminal
        print(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail=f"An unknown error occurred: {e}")