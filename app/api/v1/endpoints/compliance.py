import os
import json
from fastapi import APIRouter, HTTPException
from app.services.compliance_ml import detect_privacy_violations_ml
from app.services.compliance_regex import detect_privacy_violations_regex_op

router = APIRouter()
FOLDER_PATH = "yaml-sample-folder/All_Conversations/"

@router.post("/detect/privacy-violation/regex", response_model=dict)
def detect_privacy_violation():
    """
    Detects privacy violations in call transcripts using regex-based detection.

    Returns:
    --------
    dict:
        {
            "status_code": 200 if successful, otherwise an error code,
            "violating_call_ids": [list of call IDs where violations were detected]
        }
    """
    try:
        if not os.path.exists(FOLDER_PATH):
            raise HTTPException(status_code=404, detail="Folder not found")

        status_code, violating_calls = detect_privacy_violations_regex_op(FOLDER_PATH)

        if status_code != 200:
            raise HTTPException(status_code=status_code, detail="Regex processing error")

        return {"status_code": status_code, "violating_call_ids": violating_calls}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error accessing the folder.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON file format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/detect/privacy-violation/ml", response_model=dict)
def detect_privacy_violation_ml():
    """
    Detects privacy violations in call transcripts using an ML-based detection model.

    Returns:
    --------
    dict:
        {
            "status_code": 200 if successful, otherwise an error code,
            "violating_call_ids": [list of call IDs where violations were detected]
        }
    """
    try:
        if not os.path.exists(FOLDER_PATH):
            raise HTTPException(status_code=404, detail="Folder not found")

        status_code, violating_calls = detect_privacy_violations_ml(FOLDER_PATH)

        if status_code != 200:
            raise HTTPException(status_code=status_code, detail="Hugging Face API Error")

        return {"status_code": status_code, "violating_call_ids": violating_calls}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error accessing the folder.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON file format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
