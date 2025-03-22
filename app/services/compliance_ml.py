# app/services/compliance_ml.py

import os
import json
from fastapi import HTTPException
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Hugging Face API Configuration
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"  # Change model if needed
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}  

# Labels for classification
SENSITIVE_INFO_LABELS = ["financial_information", "account_details"]
IDENTITY_VERIFICATION_LABELS = ["identity_verification", "personal_identification"]

def query_huggingface(text):
    payload = {"inputs": text, "parameters": {"candidate_labels": SENSITIVE_INFO_LABELS + IDENTITY_VERIFICATION_LABELS}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        raise HTTPException(status_code=response.status_code, detail="Hugging Face API Error")
    
    return response.json()

def detect_privacy_violations_ml(folder_path: str):
    violating_calls = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

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
                            break

    return 200, list(set(violating_calls))  # Ensure unique call IDs

def detect_privacy_violation_ml_op():
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
