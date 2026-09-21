from ..models.local import OllamaModel
from ..models.cloud import GroqModel

class InferenceRouter:
    """
    The actual 'Brain' of the AI Cost Optimization Platform.
    Decides whether a request should be processed Locally (Brother's PC) or in the Cloud (Groq).
    """
    def __init__(self):
        self.local_model = OllamaModel()
        self.cloud_model = GroqModel()

    def route_request(self, prompt: str, strategy: str = "cheapest") -> dict:
        """
        Dynamically routes the prompt based on the user's optimization strategy!
        Returns a dict containing:
          - result_payload: the generated dictionary from the winning model
          - network_used: "local" or "cloud" string
        """
        if strategy == "cheapest":
            # Local electricity ($0.05/M) is mathematically cheaper than Cloud inference ($0.15/M)
            payload = self.local_model.generate(prompt)
            network = "local"
            
        elif strategy == "fastest":
            # Groq Cloud LPUs return responses instantly (~100ms) compared to home GPUs
            payload = self.cloud_model.generate(prompt, model="qwen/qwen3.8-27b")
            network = "cloud"
            
        elif strategy == "highest_quality":
            # A massive 27B Cloud model beats a small local 8B model natively for complex tasks
            payload = self.cloud_model.generate(prompt, model="qwen/qwen3.8-27b")
            network = "cloud"
            
        else:
            # Default to local if an unknown strategy is passed
            payload = self.local_model.generate(prompt)
            network = "local"
            
        return {
            "result_payload": payload,
            "network_used": network
        }
