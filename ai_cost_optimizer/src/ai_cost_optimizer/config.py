import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

# Replace this parameter with your Groq API key!
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "your_groq_api_key_here" 
)