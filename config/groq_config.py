import os
import time
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODELS = {
    "reasoning": "llama-3.3-70b-versatile",
    "fast": "llama-3.1-8b-instant",
    "tool": "mixtral-8x7b-32768",
    "embedding": "llama-3.3-70b-versatile"
}

@retry(stop=stop_after_attempt(3),
wait=wait_exponential(multiplier=1, min=2))
def groq_with_retry(messages):
    return get_groq_response(messages)
def get_groq_response(messages, model=MODELS["reasoning"], temperature=0.1):
    """Helper function to get responses from Groq"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=2000,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print (f"Error calling Groq API: {e}")
        return None


def test_groq_connection():
    """Test if Groq API is working"""
    try:
        response = get_groq_response(
            [{"role": "user", "content": "Test connection"}]
        )
        return response is not None
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False