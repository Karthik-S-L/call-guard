import os
import requests
from dotenv import load_dotenv
from app.models.profanity import ProfanityResponse

# Load environment variables
load_dotenv()

# Load API Key from .env
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("PROFANITY_API_URL","https://router.huggingface.co/hf-inference/models/unitary/toxic-bert")

# Ensure API key is set
if not API_KEY:
    raise ValueError("Missing API_KEY in environment variables!")

# Correct API headers
headers = {"Authorization": f"Bearer {API_KEY}"}

def detect_profanity_ml(text: str):
    """
    Detects profanity in a given text using Hugging Face's 'toxic-bert' model.

    Parameters:
    -----------
    text : str
        The input text to analyze.

    Returns:
    --------
    dict
        - is_profane (bool): True if profanity is detected, False otherwise.
        - detected_words (list): List of detected profane words or labels.
    """
    try:
        payload = {"inputs": text}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)  # 10-sec timeout

        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return ProfanityResponse(is_profane=False, detected_words=[]).model_dump()

        results = response.json()
        print(f"Input Text: {text}")
        print("Raw API Response:", results)

        # Normalize Hugging Face API response (sometimes returns nested lists)
        if isinstance(results, list) and results and isinstance(results[0], list):
            results = results[0]  # Extract inner list if nested

        detected_words = [
            r["label"] for r in results if r["label"] in ["toxic", "insult", "obscene"] and r["score"] > 0.00001
        ]

        profanity_response = {
            "is_profane": bool(detected_words),
            "detected_words": detected_words
        }

        print("Final Detection Result:", profanity_response)
        return profanity_response

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}")
        return ProfanityResponse(is_profane=False, detected_words=[]).model_dump()

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        return ProfanityResponse(is_profane=False, detected_words=[]).model_dump()
