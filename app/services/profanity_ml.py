import os
from app.models.profanity import ProfanityResponse
import requests
from dotenv import load_dotenv



# Load API Key from .env
HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://router.huggingface.co/hf-inference/models/unitary/toxic-bert"
headers = {"Authorization": "Bearer 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"}


# Ensure API key is set
if not HF_API_KEY:
    raise ValueError("Missing HF_API_KEY in environment variables!")


def detect_profanity_ml(text: str):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)
        return ProfanityResponse(is_profane=False, detected_words=[]).model_dump()

    results = response.json()
    print("results:",results)
    # Fix: Handle nested list response
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], list):
        results = results[0]  # Extract the inner list

    detected_words = [
        r["label"] for r in results if r["label"] in ["toxic", "insult", "obscene"] and r["score"] > 0.5
    ]

    return ProfanityResponse(
    is_profane=bool(detected_words),
    detected_words=detected_words
).model_dump()

