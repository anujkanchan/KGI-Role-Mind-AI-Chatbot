# Step1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List

# Define the expected request structure for the API
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


# Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

# Allowed LLM model names for safety
ALLOWED_MODEL_NAMES = ["llama-3.3-70b-versatile", "gpt-4o-mini"]

# Initialize FastAPI backend
app = FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    # Validate requested model name
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}
    
    # Extract request fields
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Create AI Agent and get response from it
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response


# Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    # Start FastAPI server at localhost:9999
    uvicorn.run(app, host="127.0.0.1", port=9999)
