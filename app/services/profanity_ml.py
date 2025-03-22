import os
from app.models.profanity import ProfanityResponse
import requests
from dotenv import load_dotenv

load_dotenv()
# Load API Key from .env
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL = "https://router.huggingface.co/hf-inference/models/unitary/toxic-bert"
headers = {"Authorization": "Bearer {HF_API_KEY}"}


# Ensure API key is set
if not HF_API_KEY:
    raise ValueError("Missing HF_API_KEY in environment variables!")


def detect_profanity_ml(text: str):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return ProfanityResponse(is_profane=False, detected_words=[]).model_dump()

    results = response.json()
    print(f"Input Text: {text}")
    print("Raw API Response:", results)

 
    if isinstance(results, list) and results and isinstance(results[0], list):
        results = results[0]  # Extract the inner list because sometime Hugging face gave [[{}]] format response.


    detected_words = [
        r["label"] for r in results if r["label"] in ["toxic", "insult", "obscene"] and r["score"] > 0.00001
    ]

    profanity_response = {
        "is_profane": bool(detected_words),
        "detected_words": detected_words
    }

    print("Final Detection Result:", profanity_response)
    return profanity_response

