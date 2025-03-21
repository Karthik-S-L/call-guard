import io
import json
import os
import zipfile
from fastapi import APIRouter, HTTPException
import yaml
from app.models.profanity import ProfanityRequest, ProfanityResponse
from app.services.profanity_regex import detect_profanity_regex
from app.services.profanity_ml import detect_profanity_ml
from app.services.profanity_llm import detect_profanity_llm

router = APIRouter()
zip_path = "yaml-sample-folder/All_Conversations.zip"

@router.post("/detect/profanity/regex", response_model=dict)
def detect_profanity_using_regex():
    try:
        folder_path = "yaml-sample-folder/All_Conversations/" 
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        profane_calls = {"agent": set(), "customer": set()}  

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):  
                file_path = os.path.join(folder_path, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)  

                call_id = filename  # Using filename as call_id

                for entry in data:
                    speaker = entry.get("speaker", "").lower()
                    text = entry.get("text", "")

                    if detect_profanity_regex(text):  # If regex detects profanity
                        if speaker == "agent":
                            profane_calls["agent"].add(call_id)
                        elif speaker == "customer":
                            profane_calls["customer"].add(call_id)

        return profane_calls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect/profanity/ml/files", response_model=dict)
def detect_profanity_using_ml():
    try:
        folder_path = "yaml-sample-folder/All_Conversations/"  # Corrected path to JSON files
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        profane_calls = {"agent": set(), "customer": set()}

        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):  # Process JSON files
                file_path = os.path.join(folder_path, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)  # Load JSON content
                    print(data)
                

                call_id = filename  # Using filename as call_id

                for entry in data:
                    speaker = entry.get("speaker", "").lower()
                    text = entry.get("text", "")

                    if detect_profanity_ml(text)["is_profane"]:  # Call ML detection
                        if speaker == "agent":
                            profane_calls["agent"].add(call_id)
                        elif speaker == "customer":
                            profane_calls["customer"].add(call_id)

        return profane_calls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect/profanity/llm", response_model=ProfanityResponse)
def detect_profanity_using_llm(request: ProfanityRequest):
    try:
        is_profane = detect_profanity_llm(request.text)
        return {"is_profane": is_profane, "detected_words": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect/profanity/compare")
def compare_profanity_detection(request: ProfanityRequest):
    regex_result = detect_profanity_regex(request.text)
    ml_result = detect_profanity_ml(request.text)
    #llm_result = detect_profanity_llm(request.text)
    
    return {
        "regex": {"is_profane": bool(regex_result), "detected_words": regex_result},
        "ml": {"is_profane": ml_result}, 
    }


'''

'''