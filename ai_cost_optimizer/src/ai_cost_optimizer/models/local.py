import time
import requests

from .base import BaseModel
from ..config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaModel(BaseModel):

    def __init__(
        self,
        host: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
    ):
        self.host = host.rstrip("/")
        self.model = model

    def generate(self, prompt: str) -> dict:

        start_time = time.perf_counter()

        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "response": data.get("response", ""),
            "model": data.get("model", self.model),
            "input_tokens": data.get("prompt_eval_count", 0),
            "output_tokens": data.get("eval_count", 0),
            "total_tokens": (
                data.get("prompt_eval_count", 0)
                + data.get("eval_count", 0)
            ),
            "latency_ms": round(latency_ms, 2),
        }