# Step1: Setup API Keys for Groq, OpenAI and Tavily
import os

# Load environment variables for API keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize LLM models from OpenAI and Groq
openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

# Initialize Tavily search tool with limited results
search_tool = TavilySearchResults(max_results=2)

# Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

# Default system behavior for AI agent
system_prompt = "Act as an AI chatbot who is smart and friendly"

# Function to dynamically get AI response based on user-selected provider
def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Choose LLM provider based on user selection
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)

    # Allow search functionality if user enables it
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create a reactive AI agent using LangGraph
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )

    # Prepare input messages for the AI agent
    state = {"messages": query}

    # Invoke the agent to process input and get output
    response = agent.invoke(state)

    # Extract AI messages from response
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    # Return the final AI-generated message
    return ai_messages[-1]
