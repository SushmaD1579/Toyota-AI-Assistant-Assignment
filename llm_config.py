"""
llm_config.py - LLM configuration and initialization
Stores API keys and initializes LLM instances.
"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLMs (using Groq for both core and final responses here)
llm_core = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
llm_final = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)

# Optionally, switch to OpenAI for final responses:
# llm_core = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
# llm_final = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
