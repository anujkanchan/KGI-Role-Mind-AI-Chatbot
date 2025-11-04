import streamlit as st
from PIL import Image
import base64

# Streamlit page setup
st.set_page_config(
    page_title="K Group Langgraph Agent UI",
    page_icon="🤖",
    layout="centered"
)

# Load and encode logo image
logo_path = r"C:\Users\AnujGaneshKanchan\Desktop\SEM 5 CSE-AIA\PBL_SEM5\AgenticAI_Bot\image\logo3_Kgroup.png"
with open(logo_path, "rb") as f:
    logo_data = f.read()
encoded_logo = base64.b64encode(logo_data).decode()

# Apply custom CSS styles
st.markdown(
    """
    <style>
    .css-18e3th9 {padding-top: 1rem;}
    .css-10trblm {text-align: center;}

    .header-box {
        position: relative;
        background: linear-gradient(135deg, #1a73e8, #34a853, #fbbc05, #ea4335);
        border-radius: 20px;
        padding: 30px 40px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        height: 140px;
    }

    .logo-corner {
        position: absolute;
        top: 10px;
        left: 10px;
        width: 70px;
        height: 65px;
    }

    .big-title {
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #f1f1f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #f0f0f0;
        text-align: center;
        margin-top: 5px;
    }

    textarea, .stTextInput, .stSelectbox, .stRadio, .stCheckbox {
        border-radius: 10px !important;
    }

    div[role="radiogroup"] > label, div[data-baseweb="checkbox"] > label {
        font-weight: 600;
    }

    .stTextArea, .stSelectbox, .stRadio, .stCheckbox {
        padding: 0.5rem;
        border-radius: 12px;
        background: #f9f9f9;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Render UI header with logo and title
st.markdown(
    f"""
    <div class="header-box" style="position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 140px;">
        <img class="logo-corner" src="data:image/png;base64,{encoded_logo}" alt="Logo">
        <div class="big-title" style="font-size: 2.5rem; font-weight: 900; color: black;">K Group India RoleMind AI</div>
        <div class="subtitle" style="font-size: 1.1rem; margin-top: 5px; color: black;"> Interact with Next-Generation Personal Agentic AI Chatbot Platform!</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Input area for system prompt
system_prompt = st.text_area(
    "📝 Define your AI Agent:",
    height=70,
    placeholder="Type your system prompt here..."
)

# Model options for both providers
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

# Provider selection
provider = st.radio("🌐 Select Provider :", ("Groq", "OpenAI"))

# Show models based on provider
if provider == "Groq":
    selected_model = st.selectbox("🤖 Select Groq Model :", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("🤖 Select OpenAI Model :", MODEL_NAMES_OPENAI)

# Option to allow Tavily web search
allow_web_search = st.checkbox("🔎 Allow Web Search")

# Input area for user query
user_query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask Anything!"
)

# Backend API endpoint
API_URL = "http://127.0.0.1:9999/chat"

# When button is pressed, send request to backend
if st.button("Ask Agent!"):
    if user_query.strip():
        # Step2: Connect with backend via URL
        import requests

        # Payload sent to backend API
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        # Send POST request to backend
        response = requests.post(API_URL, json=payload)

        # Handle backend response
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data}")
