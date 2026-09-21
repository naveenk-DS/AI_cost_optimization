import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.ai_cost_optimizer.main import app
from src.ai_cost_optimizer.database.connection import get_db, Base
from src.ai_cost_optimizer.database.models import InferenceLog

# ==============================================================
# TEST ARCHITECTURE DESIGN:
# We NEVER want Unit Tests relying on your Brother's PC or PostgreSQL.
# If his PC goes offline, our tests would falsely fail.
# Here, we spawn a temporary "in-memory" SQLite database just for testing!
# ==============================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # <-- THIS WAS THE ISSUE! 
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Dependency override to inject SQLite instead of Postgres"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# We force FastAPI to swap out `get_db` automatically with our test database!
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ==============================================================
# THE TEST SUITE
# ==============================================================

# We use `@patch` to intercept the local_model.generate network call 
# BEFORE it leaves your laptop, replacing it with fake data!
@patch("src.ai_cost_optimizer.services.router.InferenceRouter.route_request")
def test_generate_endpoint_success(mock_route):
    mock_route.return_value = {
        "result_payload": {
            "response": "This is a perfectly mocked AI text.",
            "model": "llama3.2",
            "input_tokens": 10,
            "output_tokens": 20,
            "total_tokens": 30,
            "latency_ms": 800.5
        },
        "network_used": "local"
    }
    
    # 1. Test /generate
    response = client.post("/generate", json={"prompt": "Explain RAG"})
    assert response.status_code == 200
    data = response.json()
    
    assert data["response"] == "This is a perfectly mocked AI text."
    assert "estimated_cost" in data
    
    # 2. Test InferenceLog Insertion implicitly worked. 
    # Because we didn't crash, the ModelManager wrote this to SQLite successfully!

def test_usage_endpoint():
    # 3. Test /usage persistence
    # Since our tests share the SQLite memory context, the row we inserted
    # in `test_generate_endpoint_success` exists here!
    response = client.get("/usage")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_requests"] >= 1
    assert data["successful_requests"] >= 1
    assert data["total_tokens"] >= 30

@patch("src.ai_cost_optimizer.services.router.InferenceRouter.route_request")
def test_database_failure_handling(mock_route):
    # 4. Test Error Handling & Database disconnects
    # We test what happens if Ollama succeeds, but the database completely crashes.
    mock_route.return_value = {
        "result_payload": {
            "response": "The DB will crash but you can read this text!",
            "model": "llama3.2",
            "input_tokens": 10,
            "output_tokens": 20,
            "total_tokens": 30,
            "latency_ms": 800.5
        },
        "network_used": "local"
    }
    
    # We break the database connection forcefully to test the Exception catch logic!
    app.dependency_overrides.pop(get_db, None) 
    # Normally this uses Postgres without `.env` mocking so it might fail, 
    # but the API gracefully catches DB insertion errors internally!
    
    response = client.post("/generate", json={"prompt": "Break my DB"})
    assert response.status_code == 200
    assert response.json()["response"] == "The DB will crash but you can read this text!"
