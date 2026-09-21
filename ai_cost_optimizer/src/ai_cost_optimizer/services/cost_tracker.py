import os
from decimal import Decimal

class CostTracker:
    """
    Responsibility: Pure computational logic for pricing.
    Takes token counts and model pricing and returns the predicted cost.
    Does NOT know about databases or HTTP requests.
    """
    
    def __init__(self):
        # We don't pretend local inferences are completely free. 
        # Server electricity, GPU wear, and infrastructure have real costs!
        # We use os.getenv to allow ops to configure this dynamically.
        # Fallback is set to $0.20 per 1M tokens as a placeholder infrastructure cost.
        self.local_input_price = Decimal(os.getenv("LOCAL_INPUT_PRICE_PER_1M", "0.20"))
        self.local_output_price = Decimal(os.getenv("LOCAL_OUTPUT_PRICE_PER_1M", "0.20"))
        
        # In a larger app, this might query a database to get real-time cloud pricing.
        self.pricing_registry = {
            "gpt-4o": {"input": Decimal("5.00"), "output": Decimal("15.00")},
            "qwen/qwen3.8-27b": {"input": Decimal("0.15"), "output": Decimal("0.60")},
        }

    def _get_pricing_for_model(self, model: str) -> dict:
        """Retrieves pricing based on the model name."""
        if model in self.pricing_registry:
            return self.pricing_registry[model]
        
        # If model is unknown (like llama3.2), treat it as a local infrastructure cost
        return {
            "input": self.local_input_price,
            "output": self.local_output_price
        }

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> dict:
        """
        Calculates the estimated cost based on token usage.
        
        WHY DECIMAL?
        Using Python's built-in `float` for currency leads to floating-point representation 
        errors (e.g. 0.1 + 0.2 = 0.30000000000000004). 
        The Decimal class provides exact arithmetic, which is mandatory in billing software.
        """
        if input_tokens < 0 or output_tokens < 0:
            raise ValueError("Token counts cannot be negative.")

        pricing = self._get_pricing_for_model(model)
        
        # Costs are typically priced per 1,000,000 tokens
        input_cost = (Decimal(input_tokens) / Decimal("1000000")) * pricing["input"]
        output_cost = (Decimal(output_tokens) / Decimal("1000000")) * pricing["output"]
        
        total_cost = input_cost + output_cost
        
        # Calculate Savings against GPT-4o (baseline enterprise model)
        gpt4o = self.pricing_registry.get("gpt-4o")
        baseline_input = (Decimal(input_tokens) / Decimal("1000000")) * gpt4o["input"]
        baseline_output = (Decimal(output_tokens) / Decimal("1000000")) * gpt4o["output"]
        baseline_cost = baseline_input + baseline_output
        
        cost_saved = baseline_cost - total_cost

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            # We convert the final result back to a standard python float rounded to 6 decimal places
            # so the FastAPI framework can easily convert it to JSON when returning to the user.
            "estimated_cost": float(round(total_cost, 6)),
            "cost_saved": float(round(cost_saved, 6))
        }
