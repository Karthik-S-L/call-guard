import os
import json
import requests
from typing import Tuple, List
from fastapi import HTTPException

# Load Hugging Face API details from environment variables
API_URL = os.getenv("COMPLIANCE_API_URL", "https://api-inference.huggingface.co/models/facebook/bart-large-mnli")
API_KEY = os.getenv("API_KEY", "")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Classification Labels
SENSITIVE_INFO_LABELS = ["account balance", "account number", "due amount", "outstanding balance"]
IDENTITY_VERIFICATION_LABELS = ["date of birth", "dob", "address", "social security number", "verify identity", "security question"]

def query_huggingface(text: str) -> dict:
    """
    Sends text to the Hugging Face zero-shot classification model for entity detection.

    Parameters:
    -----------
    text : str
        The input text to analyze.

    Returns:
    --------
    dict
        The JSON response containing labels and confidence scores.
    """
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Hugging Face API key not configured.")

    payload = {"inputs": text, "parameters": {"candidate_labels": SENSITIVE_INFO_LABELS + IDENTITY_VERIFICATION_LABELS}}

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=10)  # Timeout prevents hanging requests
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Hugging Face API Error")

        return response.json()

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Hugging Face API Request Failed: {str(e)}")

def detect_privacy_violations_ml(folder_path: str) -> Tuple[int, List[str]]:
    """
    Detects privacy violations using a Hugging Face zero-shot classification model.

    A violation occurs if an agent shares sensitive account details without verifying the borrower's identity.

    Parameters:
    -----------
    folder_path : str
        Path to the folder containing conversation JSON files.

    Returns:
    --------
    Tuple[int, List[str]]
        - HTTP status code (200 for success, 500 for failure).
        - List of call IDs containing privacy violations.
    """
    violating_calls = []

    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder '{folder_path}' not found.")

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        data = json.load(file)
                except json.JSONDecodeError:
                    print(f"Warning: Skipping {filename} due to JSON decoding error.")
                    continue  # Skip corrupted files

                call_id = filename
                identity_verified = False

                for entry in data:
                    speaker = entry.get("speaker", "").lower()
                    text = entry.get("text", "")

                    if speaker == "agent":
                        response = query_huggingface(text)

                        labels = response.get("labels", [])
                        scores = response.get("scores", [])

                        # Check if identity verification was mentioned
                        for label, score in zip(labels, scores):
                            if label in IDENTITY_VERIFICATION_LABELS and score > 0.7:  # Adjust confidence threshold if needed
                                identity_verified = True

                        # Check if sensitive information was shared without verification
                        for label, score in zip(labels, scores):
                            if label in SENSITIVE_INFO_LABELS and score > 0.7 and not identity_verified:
                                violating_calls.append(call_id)
                                break  # No need to check further in this file

        return 200, list(set(violating_calls))  # Ensure unique call IDs

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return 500, []  # Return failure status with an empty list

def detect_privacy_violation_ml_op():
    """
    FastAPI route handler for detecting privacy violations using machine learning.

    Returns:
    --------
    dict
        - status_code: HTTP response status.
        - violating_call_ids: List of flagged call IDs.
    """
    try:
        folder_path = "yaml-sample-folder/All_Conversations/"
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        status_code, violating_calls = detect_privacy_violations_ml(folder_path)

        if status_code != 200:
            raise HTTPException(status_code=status_code, detail="Hugging Face API Error")

        return {"status_code": status_code, "violating_call_ids": violating_calls}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
