from fastapi import APIRouter, HTTPException
from ..models.schemas import QuestionRequest, SolutionResponse, FeedbackRequest, FeedbackResponse
from ..core.guardrails import input_guardrail, output_guardrail
from ..core.math_agent import math_agent, AgentState
from ..models.database import save_feedback_entry
from datetime import datetime

router = APIRouter()

@router.post("/ask", response_model=SolutionResponse)
async def ask_math_question(request: QuestionRequest):
    """
    Endpoint to ask a math question to the agent.
    """
    # Step 1: Input Guardrail
    guardrail_check = input_guardrail(request.question)
    if not guardrail_check.is_safe:
        raise HTTPException(status_code=400, detail=guardrail_check.reason)
    
    try:
        # Step 2: Agentic Workflow
        initial_state = AgentState(question=request.question)
        final_state = math_agent.invoke(initial_state)

        # Step 3: Output Guardrail
        output_check = output_guardrail(final_state.solution)
        if not output_check.is_safe:
            raise HTTPException(status_code=500, detail="Failed output safety check.")
            
        return SolutionResponse(
            question=final_state.question,
            solution=final_state.solution,
            source=final_state.source
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest):
    """
    Endpoint to submit feedback on a generated solution.
    """
    feedback_entry = {
        "question": feedback.question,
        "solution": feedback.solution,
        "rating": feedback.rating,
        "comments": feedback.comments,
        "timestamp": datetime.now().isoformat()
    }
    
    save_feedback_entry(feedback_entry)
    
    # In a real system, this would trigger the DSPy training loop.
    # We will simulate this by simply saving the data.
    
    return FeedbackResponse(message="Feedback submitted successfully. Thank you!")