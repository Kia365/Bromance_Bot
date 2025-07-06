import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Set your TOGETHER_API_KEY in the .env file
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/completions"  # Example endpoint
MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # You can change this later

def call_llm(prompt: str) -> str:
    if not TOGETHER_API_KEY:
        return "[LLM API key not set. Please set TOGETHER_API_KEY in your .env file.]"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7
    }
    response = requests.post(TOGETHER_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["text"].strip() 