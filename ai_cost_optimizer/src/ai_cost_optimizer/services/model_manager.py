from .router import InferenceRouter
from .cost_tracker import CostTracker
from ..database.models import InferenceLog

class ModelManager:

    def __init__(self):
        self.router = InferenceRouter()
        self.cost_tracker = CostTracker()


    def generate(
        self,
        prompt: str,
        strategy: str = "cheapest",
        db=None
    ):
        # 1. Trigger the actual AI model processing via dynamic Router
        route_data = self.router.route_request(prompt, strategy=strategy)
        result = route_data["result_payload"]
        network = route_data["network_used"]
        
        # Inject the network type into the API response payload
        result["network"] = network

        # 2. Extract metrics from the provider's response
        model_used = result.get("model", "unknown")
        input_tokens = result.get("input_tokens", 0)
        output_tokens = result.get("output_tokens", 0)
        
        # 3. Request cost computations
        cost_data = self.cost_tracker.calculate_cost(
            model=model_used,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )
        
        # 4. Inject the estimated cost into the final dictionary
        result["estimated_cost"] = cost_data["estimated_cost"]
        
        # 5. Log inference to PostgreSQL
        if db is not None:
            try:
                # We map our unified dictionary data into our SQLAlchemy strict Class
                inference_record = InferenceLog(
                    provider=network,
                    model=model_used,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=result.get("total_tokens", 0),
                    latency_ms=result.get("latency_ms", 0.0),
                    estimated_cost=cost_data["estimated_cost"],
                    cost_saved=cost_data.get("cost_saved", 0.0),
                    status="success"
                )
                
                db.add(inference_record)
                db.commit()
            
            except Exception as e:
                # We rollback to cancel the broken database transaction.
                # We do NOT raise the exception here! 
                # We log it and silently let the user receive their AI text.
                db.rollback()
                print(f"DATABASE LOGGING ERROR: {e}")
            
        return result
