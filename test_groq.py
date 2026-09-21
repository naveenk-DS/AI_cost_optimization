import requests
import json
import os

token = "your_groq_api_key_here"

def check_url(url, model):
    print(f"Testing {model} on {url}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "temperature": 0.7
    }
    resp = requests.post(url, headers=headers, json=payload)
    print(resp.status_code)
    try:
        print(resp.json())
    except:
        print(resp.text)

check_url("https://api.groq.com/openai/v1/chat/completions", "llama3-8b-8192")
check_url("https://api.groq.com/openai/v1/chat/completions", "qwen/qwen3.8-27b")
