import requests

LLM_API_URL = "https://api.example.com/detect_profanity"  

def detect_profanity_llm(text: str) -> bool:
    """Detects profanity using a free AI model API."""
    try:
        response = requests.post(LLM_API_URL, json={"text": text})
        response_data = response.json()
        return response_data.get("is_profane", False)
    except Exception as e:
        print(f"Error calling LLM API: {e}")
        return False
  