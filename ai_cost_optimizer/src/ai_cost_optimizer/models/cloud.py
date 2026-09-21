import time
import requests
from typing import Dict, Any

from .base import BaseModel
from ..config import GROQ_API_KEY

class GroqModel(BaseModel):
    """
    Standardized Cloud Interface for Groq's high-speed GPU network.
    Returns exactly the same unified JSON structure as OllamaModel.
    """
    def __init__(self):
        # Groq natively supports the exact same formatting as OpenAI's API!
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        if not GROQ_API_KEY:
            raise ValueError("CRITICAL: GROQ_API_KEY is missing from config!")

    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Groq frequently decommissions older architectures.
        # As of today, qwen3.8-27b is insanely fast and highly available!
        model = kwargs.get("model", "qwen/qwen3.8-27b")
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": kwargs.get("temperature", 0.7)
        }

        start_time = time.time()
        
        # We explicitly use a Timeout!
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=60.0)
        
        # Throws HTTP 401 if the API key is incorrect!
        response.raise_for_status() 
        
        latency = (time.time() - start_time) * 1000
        data = response.json()
        
        # Parse OpenAI-style JSON output tree.
        text_response = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        
        return {
            "response": text_response,
            "model": model, 
            "input_tokens": usage.get("prompt_tokens", 0), 
            "output_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "latency_ms": round(latency, 2)
        }
