import os
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from typing import Literal, TypedDict
from .knowledge_base import search_knowledge_base
from .web_search import perform_web_search
from .config import settings
from langchain_core.output_parsers import StrOutputParser

# Import the GoogleGenerativeAI library
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Define the Agent State
class AgentState(TypedDict):
    """Represents the state of the agent's workflow."""
    question: str
    retrieved_content: str
    solution: str
    source: Literal["knowledge_base", "web_search", "error"]

# Initialize the LLM based on which key is available
if settings.GOOGLE_API_KEY:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=settings.GOOGLE_API_KEY, temperature=0.7)
elif settings.OPENAI_API_KEY:
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
else:
    raise ValueError("Neither OpenAI nor Google API key is set.")


# Define the nodes of the graph
def router_node(state: AgentState) -> dict:
    """
    Decides whether to use the knowledge base or web search.
    Returns a dictionary to update the graph state.
    """
    retrieved_content, _ = search_knowledge_base(state.get("question", ""))
    
    # Store the retrieved content in the state
    state["retrieved_content"] = retrieved_content
    
    # Logic to decide the next step
    if len(retrieved_content) > 500:
        print("INFO: Routing to Knowledge Base...")
        return {"next_step": "knowledge_base"}
    else:
        print("INFO: Routing to Web Search...")
        return {"next_step": "web_search"}

def knowledge_base_node(state: AgentState) -> dict:
    """Generates a solution from the knowledge base."""
    prompt = PromptTemplate.from_template(
        """
        You are a helpful math professor. Generate a step-by-step solution
        to the following question using the provided context.
        
        Question: {question}
        
        Context: {retrieved_content}
        
        If the context is insufficient, state that you cannot find a solution.
        """
    )
    chain = prompt | llm | StrOutputParser()
    solution_text = chain.invoke({
        "question": state["question"], 
        "retrieved_content": state["retrieved_content"]
    })
    
    state["solution"] = solution_text
    state["source"] = "knowledge_base"
    return state

def web_search_node(state: AgentState) -> dict:
    """Performs web search and generates a solution."""
    web_content = perform_web_search(state["question"])
    
    prompt = PromptTemplate.from_template(
        """
        You are a helpful math professor. Your task is to generate a step-by-step solution
        for a math problem. Use the following web search results as context.
        
        Question: {question}
        
        Web Search Results: {web_content}
        
        If the web results do not contain the answer, state that the solution could not be found.
        """
    )
    chain = prompt | llm | StrOutputParser()
    solution_text = chain.invoke({
        "question": state["question"], 
        "web_content": web_content
    })
    
    state["solution"] = solution_text
    state["source"] = "web_search"
    return state

# Build the LangGraph workflow
workflow = StateGraph(AgentState)

# Define the nodes
workflow.add_node("router", router_node)
workflow.add_node("knowledge_base", knowledge_base_node)
workflow.add_node("web_search", web_search_node)

# Set the entry point to the router
workflow.set_entry_point("router")

# Define conditional edges from the router
workflow.add_conditional_edges(
    "router",
    # The condition is based on the value returned by the router_node
    lambda state: state["next_step"],
    {"knowledge_base": "knowledge_base", "web_search": "web_search"}
)

# Connect the nodes to the end
workflow.add_edge("knowledge_base", END)
workflow.add_edge("web_search", END)

math_agent = workflow.compile()