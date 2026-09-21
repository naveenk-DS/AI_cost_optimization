# Use a lightweight python runtime specifically suited for production APIs
FROM python:3.11-slim

# Working directory inside the container
WORKDIR /app

# Upgrade pip natively
RUN pip install --upgrade pip

# We install core libraries straight via pip for the container.
# If a requirements.txt is mapped, we can use it, but for explicit safety we declare the primary stack:
RUN pip install fastapi uvicorn sqlalchemy psycopg[binary] requests python-dotenv pydantic-settings

# Copy the entire directory into the Docker /app environment
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Specify PYTHONPATH to ensure `src` modules resolve successfully
ENV PYTHONPATH=/app

# Run the web server
CMD ["uvicorn", "src.ai_cost_optimizer.main:app", "--host", "0.0.0.0", "--port", "8000"]
