# 💰 AI Inference Cost Optimization Platform

> **A hybrid AI inference orchestration platform that intelligently routes LLM requests between local Ollama inference and cloud-based Groq inference based on cost, speed, and quality requirements.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)](https://ollama.com/)
[![Groq](https://img.shields.io/badge/Groq-Cloud%20Inference-orange)](https://groq.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)

---

## 🧠 Overview

Modern GenAI applications can become expensive when every request is sent to a cloud LLM.

At the same time, local inference can provide extremely low marginal inference cost but may have higher latency or limited compute resources.

This project explores a practical solution:

> **Choose the appropriate inference layer for each request instead of sending every request to the same model provider.**

The **AI Inference Cost Optimization Platform** acts as an orchestration layer between the application and multiple LLM inference providers.

It currently supports:

* 🖥️ Local LLM inference through Ollama
* ☁️ Cloud inference through Groq
* 🧠 Strategy-based model routing
* 💰 Request-level cost tracking
* ⚡ Fast cloud inference
* 🔄 Route failover
* 🧮 High-precision financial calculations
* 🗄️ PostgreSQL persistence
* 📊 Analytics dashboard
* 🚀 FastAPI backend
* 🐳 Docker Compose deployment

The current implementation uses a hybrid-cloud architecture where local Ollama inference and Groq cloud inference are treated as alternative execution paths.

---

# 🎯 Problem Statement

LLM applications commonly face three problems:

### 1. Cloud inference cost

Sending every request to a premium cloud model can increase API expenditure.

### 2. Local inference limitations

Local models can reduce external API expenditure, but available hardware can introduce latency and throughput constraints.

### 3. No visibility into inference economics

Without request-level tracking, it is difficult to understand:

```text
Which model handled the request?
How much did the request cost?
How many tokens were processed?
Which routing strategy was used?
How much local inference was used?
How much cloud inference was used?
```

This project addresses these problems through a centralized inference router and cost-tracking layer.

---

# 💡 Solution

Instead of:

```text
User
  │
  ▼
Cloud LLM
  │
  ▼
Response
```

the application uses:

```text
                    ┌─────────────────┐
                    │      USER       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │   API Gateway   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Model Manager  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Inference Router│
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
         Cheapest         Fastest       Highest Quality
             │               │                │
             ▼               ▼                ▼
         Ollama            Groq             Groq
             │               │                │
             └───────────────┼────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Cost Tracker   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Dashboard    │
                    └─────────────────┘
```

The repository's current architecture explicitly follows this model-manager → inference-router → local/cloud provider → cost tracker → PostgreSQL → dashboard flow.

---

# ✨ Key Features

## 🧠 1. Hybrid LLM Inference

The platform supports two inference paths:

### Local

```text
Application
     ↓
Inference Router
     ↓
Ollama
     ↓
Local LLM
```

### Cloud

```text
Application
     ↓
Inference Router
     ↓
Groq API
     ↓
Cloud LLM
```

This allows the application to use local infrastructure when appropriate while retaining access to high-speed cloud inference.

---

# 💰 2. Cost-Aware Inference

The system tracks the financial cost associated with inference requests.

Instead of treating an LLM response as simply:

```text
prompt → response
```

the platform tracks the economics around the request.

Conceptually:

```text
Request
   │
   ├── Provider
   ├── Model
   ├── Input Tokens
   ├── Output Tokens
   ├── Token Cost
   └── Total Cost
```

The implementation uses Python's `Decimal` type for financial calculations so small values such as `$0.00015` are not affected by ordinary floating-point representation issues.

---

# ⚡ 3. Strategy-Based Routing

The inference router supports different execution strategies.

## Cheapest

```text
Strategy: cheapest
        ↓
Local Ollama
```

The project documentation currently maps the `cheapest` strategy to local Ollama inference.

---

## Fastest

```text
Strategy: fastest
        ↓
Groq
```

The current architecture maps the `fastest` strategy to Groq cloud inference.

---

## Highest Quality

```text
Strategy: highest_quality
        ↓
Groq
```

The current routing documentation also maps `highest_quality` to the cloud inference path.

---

# 🔄 4. Failover

A production-style inference system should not fail completely because one provider becomes unavailable.

NAVIX's cost-optimization project therefore wraps inference routes with error handling.

Conceptually:

```text
Request
   ↓
Primary Route
   │
   ├── Success ──────→ Response
   │
   └── Failure
          ↓
       Fallback
          ↓
       Response
```

The current project documentation describes safe `try/except` handling around inference routes so the application can remain available when a selected route fails.

---

# 🗄️ 5. PostgreSQL Cost Persistence

Inference metrics are persisted into PostgreSQL.

Architecture:

```text
LLM Provider
     ↓
Response
     ↓
Cost Tracker
     ↓
PostgreSQL
     ↓
Analytics
```

This allows request-level inference information to be retained for later analysis.

The project is configured to use PostgreSQL through SQLAlchemy-compatible connection strings.

---

# 📊 6. Analytics Dashboard

The platform includes a browser-based dashboard.

The dashboard communicates with the FastAPI backend and provides an interface for observing the inference system.

Current architecture:

```text
PostgreSQL
     ↓
Analytics Layer
     ↓
FastAPI
     ↓
Dashboard
```

The project describes the UI as a glassmorphism-style dashboard implemented with native CSS and REST API requests.

Dashboard:

```text
http://127.0.0.1:8000/
```

---

# 🚀 7. FastAPI Backend

The platform is exposed through a FastAPI application.

FastAPI provides the central API layer:

```text
Client
  ↓
FastAPI
  ↓
Model Manager
  ↓
Inference Router
  ↓
LLM Provider
```

API documentation is available through Swagger:

```text
http://127.0.0.1:8000/docs
```

The current project instructions use Uvicorn to launch:

```text
src.ai_cost_optimizer.main:app
```

with FastAPI serving on port `8000`.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────┐
                         │      Client     │
                         │  Web / API / UI │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         │    REST API     │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Model Manager  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Inference Router│
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
         Cheapest              Fastest          Highest Quality
              │                   │                   │
              ▼                   ▼                   ▼
          ┌────────┐          ┌────────┐          ┌────────┐
          │ Ollama │          │ Groq   │          │ Groq   │
          │ Local  │          │ Cloud  │          │ Cloud  │
          └───┬────┘          └───┬────┘          └───┬────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Cost Tracker   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Dashboard     │
                         └─────────────────┘
```

---

# 🔄 End-to-End Request Flow

Consider:

```text
"Summarize this document"
```

The request follows:

```text
1. Client
      ↓
2. FastAPI
      ↓
3. Model Manager
      ↓
4. Inference Router
      ↓
5. Strategy Evaluation
      ↓
6. Provider Selection
      ↓
7. Ollama / Groq
      ↓
8. Model Response
      ↓
9. Token / Cost Calculation
      ↓
10. PostgreSQL
      ↓
11. API Response
      ↓
12. Dashboard Analytics
```

This makes inference routing and its associated cost observable rather than hidden inside the application.

---

# 🧮 Cost Calculation

A simplified cost model can be represented as:

```text
Input Cost
    =
Input Tokens × Input Token Price


Output Cost
    =
Output Tokens × Output Token Price


Total Cost
    =
Input Cost + Output Cost
```

For example:

```text
Input Tokens:      1,000
Output Tokens:       500

Input Price:      $X / 1M tokens
Output Price:     $Y / 1M tokens
```

Then:

```text
Total Cost =
(1000 / 1,000,000 × X)
+
(500 / 1,000,000 × Y)
```

The implementation uses `Decimal` rather than standard floating-point arithmetic for financial calculations.

---

# 🧠 Why Hybrid Inference?

A hybrid architecture provides an important engineering trade-off.

| Inference Layer | Main Advantage                        | Main Trade-off                         |
| --------------- | ------------------------------------- | -------------------------------------- |
| Local Ollama    | Local control / low marginal API cost | Hardware and latency constraints       |
| Groq            | Fast cloud inference                  | API usage cost and external dependency |

The objective is therefore not simply:

> "Always use local."

or:

> "Always use cloud."

Instead, the platform provides a routing layer where the execution strategy determines which inference path should be used.

---

# 🛠️ Technology Stack

| Layer                 | Technology              |
| --------------------- | ----------------------- |
| Programming Language  | Python                  |
| API Framework         | FastAPI                 |
| ASGI Server           | Uvicorn                 |
| Local LLM             | Ollama                  |
| Cloud LLM             | Groq                    |
| Database              | PostgreSQL              |
| Database Layer        | SQLAlchemy              |
| Financial Calculation | Python Decimal          |
| Frontend              | HTML / CSS / JavaScript |
| API Communication     | REST                    |
| Containerization      | Docker                  |
| Orchestration         | Docker Compose          |
| Testing               | Python test scripts     |

The repository's current documentation confirms FastAPI, Ollama, Groq, PostgreSQL, Docker Compose, REST-based dashboard communication, and `Decimal`-based cost calculations.

---

# 📁 Project Structure

The repository currently has the following top-level structure:

```text
AI_cost_optimization/
│
├── ai_cost_optimizer/
│
│   └── src/
│       └── ai_cost_optimizer/
│
├── test_groq.py
│
└── test_postgres.py
```

The main application is located inside:

```text
ai_cost_optimizer/
```

and the repository currently includes dedicated tests for Groq connectivity and PostgreSQL connectivity.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/naveenk-DS/AI_cost_optimization.git
cd AI_cost_optimization
```

---

# 🐍 2. Python Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Activate on Linux/macOS:

```bash
source .venv/bin/activate
```

Install the project's dependencies according to the dependency configuration included in the project.

---

# 🧠 3. Install Ollama

Install Ollama:

```text
https://ollama.com/
```

Start the Ollama service and pull the local model required by your configuration.

Example:

```bash
ollama pull llama3.2
```

Verify Ollama:

```bash
ollama list
```

The current project architecture uses Ollama for the local inference path.

---

# ☁️ 4. Configure Groq

Create a Groq API key through the Groq platform.

Set:

```env
GROQ_API_KEY="your_groq_api_key"
```

Do not commit the API key to GitHub.

---

# 🗄️ 5. PostgreSQL

Install PostgreSQL or run it using Docker.

Example connection configuration:

```env
DATABASE_URL="postgresql+psycopg://postgres:password@localhost:5432/ai_costs"
```

The project's documented configuration uses a PostgreSQL SQLAlchemy connection string.

---

# 🔐 Environment Variables

Create:

```text
.env
```

Example:

```env
# Local LLM
OLLAMA_BASE_URL="http://127.0.0.1:11434"

# Database
DATABASE_URL="postgresql+psycopg://postgres:password@localhost:5432/ai_costs"

# Cloud LLM
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxx"
```

For a second machine running Ollama on your LAN, the Ollama URL can point to that machine:

```env
OLLAMA_BASE_URL="http://192.168.x.x:11434"
```

The original project documentation demonstrates this LAN-based Ollama configuration.

---

# ▶️ Run Locally

From the project root:

### Windows PowerShell

```powershell
$env:PYTHONPATH="."
python -m uvicorn src.ai_cost_optimizer.main:app --reload
```

### Linux/macOS

```bash
export PYTHONPATH=.
python -m uvicorn src.ai_cost_optimizer.main:app --reload
```

The project's current startup instructions use this Uvicorn module path.

---

# 🌐 Access the Application

After starting the server:

### Dashboard

```text
http://127.0.0.1:8000/
```

### Swagger API Documentation

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

The dashboard and Swagger endpoints are documented by the repository.

---

# 🐳 Docker Deployment

The project is designed to run as a containerized service.

Start:

```bash
docker-compose up --build -d
```

The documented Docker setup launches the FastAPI service together with a PostgreSQL container.

Check running containers:

```bash
docker ps
```

View logs:

```bash
docker-compose logs -f
```

Stop:

```bash
docker-compose down
```

---

# 🧪 Testing

The repository includes:

```text
test_groq.py
test_postgres.py
```

These provide basic validation for the external inference provider and database connectivity.

Run:

```bash
python test_groq.py
```

and:

```bash
python test_postgres.py
```

Use these before launching the complete application to verify that the required infrastructure is reachable.

---

# 🔍 Example Routing

## Example 1 — Cost Priority

```text
Request
   ↓
Strategy = cheapest
   ↓
Ollama
   ↓
Local LLM
   ↓
Cost Tracker
   ↓
PostgreSQL
```

---

## Example 2 — Speed Priority

```text
Request
   ↓
Strategy = fastest
   ↓
Groq
   ↓
Cloud LLM
   ↓
Cost Tracker
   ↓
PostgreSQL
```

---

## Example 3 — Quality Priority

```text
Request
   ↓
Strategy = highest_quality
   ↓
Groq
   ↓
Cloud Model
   ↓
Cost Tracker
   ↓
PostgreSQL
```

These routing strategies reflect the current architecture documented in the repository.

---

# 📊 What the Dashboard Represents

The dashboard is intended to make inference economics visible.

Conceptually, the analytics layer can expose:

```text
Total Requests
Total Tokens
Local Requests
Cloud Requests
Total Cost
Average Cost
Provider Distribution
Model Distribution
```

The purpose is to answer questions such as:

```text
How many requests used local inference?

How many requests used cloud inference?

Which provider handled the requests?

How much did inference cost?

Which routing strategy was selected?
```

---

# 🧠 Engineering Concepts Demonstrated

This project demonstrates practical GenAI engineering concepts including:

### LLM Infrastructure

* Local LLM inference
* Cloud LLM inference
* Multi-provider inference
* Model abstraction
* Inference routing

### AI Cost Engineering

* Token-based cost calculation
* Provider-aware pricing
* Cost tracking
* Cost-aware routing
* Local vs cloud trade-offs

### Backend Engineering

* FastAPI
* REST APIs
* Uvicorn
* Request orchestration
* Error handling

### Data Engineering

* PostgreSQL
* Persistent inference metrics
* Analytics data
* Database connectivity

### DevOps

* Docker
* Docker Compose
* Environment configuration
* Service orchestration

### Reliability

* Provider failover
* Error handling
* Local/cloud fallback architecture

---

# 🔐 Security

Never commit:

```text
.env
API keys
Database passwords
Private tokens
Credentials
```

Use environment variables instead:

```env
GROQ_API_KEY="..."
DATABASE_URL="..."
OLLAMA_BASE_URL="..."
```

If Ollama is exposed over a LAN, ensure the host and network configuration are appropriately secured.

For production deployment, additional controls should be considered:

* Authentication
* Authorization
* Rate limiting
* Secret management
* HTTPS
* Network isolation
* Database access control
* API request validation
* Audit logging

---

# ⚠️ Important Production Considerations

This repository demonstrates an AI inference cost-optimization architecture.

Before using it as a production financial-control system, pricing data, provider APIs, model availability, failure behavior, and token accounting should be validated against the current provider documentation.

Actual cost savings depend on:

```text
Request distribution
+
Model pricing
+
Token usage
+
Local hardware cost
+
Cloud latency
+
Routing strategy
+
Provider availability
```

Therefore, the system should be evaluated using real workloads and measured benchmarks rather than assuming a fixed percentage of savings.

---

# 📈 Evaluation Strategy

A useful evaluation framework is:

```text
                 AI Request Dataset
                         │
                         ▼
                ┌─────────────────┐
                │ Routing System  │
                └────────┬────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
         Local LLM               Cloud LLM
             │                       │
             ▼                       ▼
         Measure                  Measure
             │                       │
       ┌─────┼─────┐           ┌─────┼─────┐
       │     │     │           │     │     │
     Cost  Latency Quality    Cost Latency Quality
       │     │     │           │     │     │
       └─────┴─────┴───────────┴─────┴─────┘
                         │
                         ▼
                  Compare Results
```

Important metrics include:

* Cost per request
* Cost per 1K tokens
* Input tokens
* Output tokens
* Latency
* Error rate
* Provider utilization
* Response quality
* Local vs cloud request ratio

---

# 🗺️ Future Roadmap

## Routing

* [ ] Dynamic complexity scoring
* [ ] Automatic model selection
* [ ] Quality-aware routing
* [ ] Latency-aware routing
* [ ] Budget-aware routing
* [ ] Multi-provider routing

## Cost Optimization

* [ ] Token-level cost dashboards
* [ ] Monthly budget limits
* [ ] Budget alerts
* [ ] Cost forecasting
* [ ] Cost anomaly detection
* [ ] Historical cost comparison

## AI

* [ ] More LLM providers
* [ ] OpenAI integration
* [ ] Anthropic integration
* [ ] Gemini integration
* [ ] More local models
* [ ] Model benchmarking

## Observability

* [ ] Request tracing
* [ ] Latency monitoring
* [ ] Provider health monitoring
* [ ] Model performance metrics
* [ ] Request-level logs
* [ ] Optimization recommendations

## Infrastructure

* [ ] Kubernetes deployment
* [ ] Horizontal scaling
* [ ] Redis caching
* [ ] Background workers
* [ ] Production authentication
* [ ] Distributed inference routing

---

# 🔬 Future Intelligent Router

The current strategy-based routing can be extended into a dynamic decision engine.

For example:

```text
                   User Request
                        │
                        ▼
                Complexity Analyzer
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
        Simple        Medium        Complex
          │             │             │
          ▼             ▼             ▼
       Local LLM     Local/Cloud     Cloud LLM
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  Cost + Quality
                     Monitor
```

The future objective would be to optimize multiple variables simultaneously:

```text
Cost
Latency
Quality
Availability
Hardware Utilization
Token Usage
```

rather than optimizing cost alone.

---

# 🏆 Project Highlights

This project demonstrates a practical approach to **LLM infrastructure optimization**.

Instead of building another chatbot, the system focuses on the infrastructure layer behind AI applications:

```text
                AI APPLICATION
                      │
                      ▼
              ┌───────────────┐
              │ AI Cost Layer │
              └───────┬───────┘
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
      Local AI                 Cloud AI
       Ollama                   Groq
          │                       │
          └───────────┬───────────┘
                      ▼
                Cost Tracking
                      │
                      ▼
                  PostgreSQL
                      │
                      ▼
                 Analytics
```

The main engineering idea is:

> **LLM inference should be treated as an infrastructure resource that can be measured, routed, and optimized.**

---

# 💼 Why This Project Matters for GenAI Engineering

A typical GenAI application focuses mainly on:

```text
Prompt → LLM → Response
```

This project goes one level deeper:

```text
Application
     ↓
Inference Gateway
     ↓
Model Routing
     ↓
Provider Selection
     ↓
Inference
     ↓
Token Accounting
     ↓
Cost Calculation
     ↓
Persistence
     ↓
Analytics
```

This demonstrates understanding of:

* LLM inference infrastructure
* Multi-provider architecture
* Cost engineering
* API development
* Database persistence
* Reliability
* Containerization
* AI system observability

---

# 👨‍💻 Author

## Naveen K

**AI / ML & GenAI Engineer**

Areas of interest:

```text
Artificial Intelligence
Machine Learning
Generative AI
LLMs
RAG
AI Agents
LLM Infrastructure
Inference Optimization
Model Optimization
Computer Vision
NLP
FastAPI
Local AI
AI Automation
```

GitHub:

```text
https://github.com/naveenk-DS
```

Project:

```text
https://github.com/naveenk-DS/AI_cost_optimization
```

---

# ⭐ Support

If you find this project useful for learning or experimentation:

* ⭐ Star the repository
* 🐛 Report issues
* 💡 Suggest improvements
* 🔧 Submit pull requests
* 📚 Experiment with new routing strategies

---

# 📄 License

See the repository's license file for the applicable license terms.

---

## 🚀 AI Inference Cost Optimization

> **Route intelligently. Track everything. Optimize AI inference.**
