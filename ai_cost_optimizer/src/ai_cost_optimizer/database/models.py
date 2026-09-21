from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Numeric
from datetime import datetime, timezone
import uuid

from .connection import Base

class InferenceLog(Base):
    """
    SQLAlchemy ORM Model mapping to the 'inference_logs' table.
    Records every single AI generation event for analytics and billing.
    """
    __tablename__ = "inference_logs"

    # UUID primary key securely distributes database load compared to auto-incrementing integers
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Indexed so we can quickly look up logs related to a specific user's web request
    request_id = Column(String, nullable=True, index=True) 
    
    # We use UTC timezone exclusively to prevent timezone disasters across servers
    # It is indexed because time-series queries (e.g., billing month) heavily filter by timestamp!
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    provider = Column(String, nullable=False) # e.g. "ollama", "openai"
    model = Column(String, nullable=False, index=True)    # e.g. "llama3.2" (Indexed for usage queries)
    
    # Tracking metrics
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    latency_ms = Column(Float, default=0.0)
    
    # Numeric provides EXACT precision vs Float. Perfect for money because 
    # floats cause rounding errors in sums. 10 digits total, 6 decimal places.
    estimated_cost = Column(Numeric(precision=10, scale=6), default=0.0)
    cost_saved = Column(Numeric(precision=10, scale=6), default=0.0)
    
    # Reliability metrics
    status = Column(String, default="success", nullable=False) # "success" or "error"
    
    # Text allows unlimited length compared to standard String, which is ideal for massive stack traces
    error_message = Column(Text, nullable=True)
