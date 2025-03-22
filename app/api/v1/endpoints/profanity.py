import os
import json
from fastapi import APIRouter, HTTPException, Depends
from app.models.profanity import ProfanityRequest, ProfanityResponse
from app.services.profanity_regex import detect_profanity_regex
from app.services.profanity_ml import detect_profanity_ml
from app.services.profanity_llm import detect_profanity_llm

router = APIRouter()
FOLDER_PATH = "yaml-sample-folder/All_Conversations/"

@router.post("/detect/profanity/regex", response_model=dict)
def detect_profanity_using_regex():
    """
    Detects profanity in conversation files using regex-based pattern matching.

    Returns:
    --------
    dict:
        {
            "agent": [list of call IDs with agent profanity],
            "customer": [list of call IDs with customer profanity]
        }
    """
    try:
        if not os.path.exists(FOLDER_PATH):
            raise HTTPException(status_code=404, detail="Folder not found")

        profane_calls = {"agent": set(), "customer": set()}

        for filename in os.listdir(FOLDER_PATH):
            if filename.endswith(".json"):
                file_path = os.path.join(FOLDER_PATH, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                call_id = filename

                for entry in data:
                    speaker = entry.get("speaker", "").lower()
                    text = entry.get("text", "")

                    if detect_profanity_regex(text):  # If regex detects profanity
                        if speaker == "agent":
                            profane_calls["agent"].add(call_id)
                        elif speaker == "customer":
                            profane_calls["customer"].add(call_id)

        return {"agent": list(profane_calls["agent"]), "customer": list(profane_calls["customer"])}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error accessing JSON files.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON file format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/detect/profanity/ml/files", response_model=dict)
def detect_profanity_using_ml():
    """
    Detects profanity in conversation files using an ML model.

    Returns:
    --------
    dict:
        {
            "agent": [list of call IDs with agent profanity],
            "customer": [list of call IDs with customer profanity]
        }
    """
    try:
        if not os.path.exists(FOLDER_PATH):
            raise HTTPException(status_code=404, detail="Folder not found")

        profane_calls = {"agent": set(), "customer": set()}

        for filename in os.listdir(FOLDER_PATH):
            if filename.endswith(".json"):
                file_path = os.path.join(FOLDER_PATH, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                call_id = filename

                for entry in data:
                    speaker = entry.get("speaker", "").lower()
                    text = entry.get("text", "")

                    ml_result = detect_profanity_ml(text)
                    if isinstance(ml_result, dict) and ml_result.get("is_profane"):
                        if speaker == "agent":
                            profane_calls["agent"].add(call_id)
                        elif speaker == "customer":
                            profane_calls["customer"].add(call_id)

        return {"agent": list(profane_calls["agent"]), "customer": list(profane_calls["customer"])}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error accessing JSON files.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON file format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/detect/profanity/llm", response_model=ProfanityResponse)
def detect_profanity_using_llm(request: ProfanityRequest):
    """
    Detects profanity in a given text using an LLM-based model.

    Parameters:
    -----------
    request : ProfanityRequest
        The input text to analyze.

    Returns:
    --------
    ProfanityResponse:
        - is_profane (bool): True if profanity is detected, False otherwise.
        - detected_words (list): List of detected profane words (if applicable).
    """
    try:
        is_profane = detect_profanity_llm(request.text)
        return ProfanityResponse(is_profane=is_profane, detected_words=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/detect/profanity/compare", response_model=dict)
def compare_profanity_detection(request: ProfanityRequest):
    """
    Compares profanity detection results from Regex and ML approaches.

    Parameters:
    -----------
    request : ProfanityRequest
        The input text to analyze.

    Returns:
    --------
    dict:
        {
            "regex": {"is_profane": bool, "detected_words": list},
            "ml": {"is_profane": bool, "detected_words": list}
        }
    """
    try:
        regex_result = detect_profanity_regex(request.text)
        ml_result = detect_profanity_ml(request.text)

        return {
            "regex": {"is_profane": bool(regex_result), "detected_words": regex_result},
            "ml": {"is_profane": ml_result.get("is_profane", False), "detected_words": ml_result.get("detected_words", [])},
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
