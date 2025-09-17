from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from typing import List, Dict, Any, Literal
from langchain_core.tools import tool

from typing import TypedDict, Annotated, Literal
import operator

from .knowledge_base import search_knowledge_base
from .web_search import perform_web_search

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Define the State for LangGraph
class AgentState(TypedDict):
    question: str
    retrieved_content: str
    solution: str
    source: Literal["knowledge_base", "web_search"]
    
    # Make sure to handle the case where state fields might be missing
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "retrieved_content" not in self:
            self["retrieved_content"] = ""
        if "solution" not in self:
            self["solution"] = ""
        if "source" not in self:
            self["source"] = ""
 
def agent_router(state: AgentState) -> str:
    """Decides whether to search the knowledge base or the web."""
    retrieved_content, _ = search_knowledge_base(state.question)
    
    # Update the state with the retrieved content before routing
    state["retrieved_content"] = retrieved_content
    
    if len(state["retrieved_content"]) > 500:
        print("Routing to Knowledge Base...")
        return "kb_search"
    else:
        print("Routing to Web Search...")
        return "web_search"

def kb_solution_generator(state: AgentState) -> AgentState:
    """Generates a solution from the knowledge base content."""
    prompt = PromptTemplate.from_template(
        """
        You are a helpful math professor. Generate a step-by-step solution
        to the following question using the provided context from the knowledge base.

        Question: {question}

        Context: {retrieved_content}

        If the context is insufficient, state that you cannot find a solution.
        """
    )
    chain = prompt | llm
    solution_text = chain.invoke({"question": state.question, "retrieved_content": state.retrieved_content})

    state.solution = solution_text
    state.source = "knowledge_base"
    return {"solution": state.solution, "source": state.source}

def web_solution_generator(state: AgentState) -> AgentState:
    """Performs web search and generates a solution."""
    web_content = perform_web_search(state.question)

    prompt = PromptTemplate.from_template(
        """
        You are a helpful math professor. Your task is to generate a step-by-step solution
        for a math problem. Use the following web search results as context.

        Question: {question}

        Web Search Results: {web_content}

        Ensure the response is educational and simplified. If the web results do not contain
        the answer, do not guess. State that the solution could not be found.
        """
    )

    chain = prompt | llm
    solution_text = chain.invoke({"question": state.question, "web_content": web_content})

    state.solution = solution_text
    state.source = "web_search"
    return {"solution": state.solution, "source": state.source}

workflow = StateGraph(AgentState)

# Add the nodes (functions that modify the state)
workflow.add_node("kb_solution_generator", kb_solution_generator)
workflow.add_node("web_solution_generator", web_solution_generator)

# Define the entry point and the conditional edges for routing
workflow.set_entry_point("router")
workflow.add_conditional_edges(
    "router",
    # This is the conditional function for routing
    agent_router,
    # These are the mapping from the router's return value to the next node
    {"kb_search": "kb_solution_generator", "web_search": "web_solution_generator"}
)

# Define the final edge to end the graph
workflow.add_edge("kb_solution_generator", END)
workflow.add_edge("web_solution_generator", END)

math_agent = workflow.compile()