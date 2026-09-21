# AI Inference Cost Optimization Platform

This is a production-grade backend orchestration system capable of routing AI inference requests between local hardware accelerators (**Ollama via LAN**) and Cloud LLM providers (**Groq via WAN**). 

The platform intercepts prompts and intelligently delegates them based on specific rules (e.g., fastest response layer, cheapest array) while simultaneously logging precise fractional-cent financial metrics into an attached PostgreSQL database.

## 🧠 Architecture Overview

The platform uses a Hybrid-Cloud architecture:

```mermaid
graph TD;
    USER(Web App / User) -->|Prompt + Strategy| API[FastAPI Server]
    API -->|Generate Request| MM[ModelManager]
    MM -->|Rule Mapping| IR{Inference Router}
    
    IR -- Strategy: 'cheapest' --> LLM_LOCAL[Ollama: Llama-3.2]
    LLM_LOCAL -.->|Local Network| GPU(Brother's PC RTX 3060)
    
    IR -- Strategy: 'fastest' --> LLM_CLOUD[Groq API]
    LLM_CLOUD -.->|External Network| CLOUD(Groq LPUs)
    
    IR -- Strategy: 'highest_quality' --> LLM_CLOUD
    
    LLM_LOCAL -->|Response + Tokens| TR[Cost Tracker Engine]
    LLM_CLOUD -->|Response + Tokens| TR
    
    TR -->|Total Computation Math| DB[(PostgreSQL)]
    DB -.->|Analytics Stream| Dash[Glassmorphism Dashboard]
```

## ✨ Features
- **Inference Router**: Actively bounces payloads between local hardware and wide-area networks depending on defined strategy.
- **Failover Security**: If a route fails, the server uses safe try/except bounds to ensure the application stays online.
- **Financial Precision**: Incorporates Python's native `Decimal` library, ensuring calculations for "$0.00015" never generate floating-point rounding errors.
- **Web Dashboard**: An ultra-sleek, native Glassmorphism CSS UI interacting cleanly with the API using Vanilla REST requests.
- **Microservice Ready**: Fully Dockerized utilizing Compose.

## 🚀 Setup & Execution

### 1. Environment Configurations
Rename `.env.example` to `.env` and map your credentials.  
```env
# Optional Local Networking
OLLAMA_BASE_URL="http://192.168.29.13:11434"

# Postgres (Or leave blank to auto-generate local SQLite file via standard pipeline logic)
DATABASE_URL="postgresql+psycopg://postgres:admin@192.168.29.13:5433/ai_costs"

# Cloud Networking
GROQ_API_KEY="gsk_xxxxx"
```

### 2. Standalone Terminal Launch
```bash
$env:PYTHONPATH="."
python -m uvicorn src.ai_cost_optimizer.main:app --reload 
```

### 3. Docker Launch (Production)
Automatically spins up the FastAPI container alongside a dedicated Alpine PostgreSQL image.
```bash
docker-compose up --build -d
```

### Accessing the System
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Analytics Dashboard**: `http://127.0.0.1:8000/`
