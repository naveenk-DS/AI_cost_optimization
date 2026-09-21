from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..services.model_manager import ModelManager
from ..database.connection import get_db
from ..database.models import InferenceLog

router = APIRouter()

# The manager handles all routing logic so the API endpoint remains clean
model_manager = ModelManager()

class GenerateRequest(BaseModel):
    prompt: str
    strategy: str = "cheapest"


@router.post("/generate")
def generate(request: GenerateRequest, db: Session = Depends(get_db)):
    result = model_manager.generate(
        prompt=request.prompt,
        strategy=request.strategy,
        db=db
    )
    return result


@router.get("/usage")
def get_total_usage(db: Session = Depends(get_db)):
    """
    SQLAlchemy analytics query aggregating total usage metrics across all models.
    """
    try:
        # 1. We ask PostgreSQL to dynamically SUM and COUNT all values in the table.
        # This is 100x faster than downloading all rows into Python and doing the math.
        metrics = db.query(
            func.count(InferenceLog.id).label("total_requests"),
            func.sum(InferenceLog.input_tokens).label("total_input_tokens"),
            func.sum(InferenceLog.output_tokens).label("total_output_tokens"),
            func.sum(InferenceLog.total_tokens).label("total_tokens"),
            func.avg(InferenceLog.latency_ms).label("average_latency_ms"),
            func.sum(InferenceLog.estimated_cost).label("total_estimated_cost"),
            func.sum(InferenceLog.cost_saved).label("total_cost_saved")
        ).first()
        
        # 2. Grab status counts and compute aggregations
        successful = db.query(InferenceLog).filter(InferenceLog.status == "success").count()
        failed = db.query(InferenceLog).filter(InferenceLog.status == "error").count()
        local_reqs = db.query(InferenceLog).filter(InferenceLog.provider == "local").count()
        cloud_reqs = db.query(InferenceLog).filter(InferenceLog.provider == "cloud").count()
        
        success_rate = (successful / metrics.total_requests * 100.0) if metrics.total_requests else 0.0

        # 3. Handle cases where the DB is completely empty (metrics sum returns None)
        return {
            "total_requests": metrics.total_requests or 0,
            "successful_requests": successful,
            "failed_requests": failed,
            "success_rate": round(success_rate, 2),
            "local_requests": local_reqs,
            "cloud_requests": cloud_reqs,
            "total_input_tokens": metrics.total_input_tokens or 0,
            "total_output_tokens": metrics.total_output_tokens or 0,
            "total_tokens": metrics.total_tokens or 0,
            "average_latency_ms": round(metrics.average_latency_ms or 0, 2),
            "total_estimated_cost": float(metrics.total_estimated_cost or 0.0),
            "total_cost_saved": float(metrics.total_cost_saved or 0.0)
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail="Cost Analytics Database is currently offline.")

@router.get("/usage/models")
def get_usage_by_model(db: Session = Depends(get_db)):
    """
    SQLAlchemy GROUP BY query aggregating usage split uniquely by model names and providers.
    """
    try:
        query = db.query(
            InferenceLog.provider,
            InferenceLog.model,
            func.count(InferenceLog.id).label("requests"),
            func.sum(InferenceLog.total_tokens).label("total_tokens"),
            func.sum(InferenceLog.estimated_cost).label("cost")
        ).group_by(InferenceLog.provider, InferenceLog.model).all()
        
        results = []
        # Loop over the raw query results and map them into neat dictionaries for JSON
        for row in query:
            results.append({
                "provider": row.provider,
                "model": row.model,
                "total_requests": row.requests,
                "total_tokens": row.total_tokens or 0,
                "total_estimated_cost": float(row.cost or 0.0)
            })
            
        return {"data": results}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Cost Analytics Database is currently offline.")
