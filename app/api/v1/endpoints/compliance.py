import os
import json
from fastapi import APIRouter, HTTPException
from app.services.compliance_ml import detect_privacy_violations_ml
from app.services.compliance_regex import detect_privacy_violations_regex_op

router = APIRouter()

@router.post("/detect/privacy-violation/regex")
def detect_privacy_violation():
    try:
        folder_path = "yaml-sample-folder/All_Conversations/"
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        status_code,violating_calls = detect_privacy_violations_regex_op(folder_path)
        return {"status_code":status_code,"violating_call_ids": violating_calls}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/detect/privacy-violation/ml")
def detect_privacy_violation_ml():
    try:
        folder_path = "yaml-sample-folder/All_Conversations/"
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        status_code, violating_calls = detect_privacy_violations_ml(folder_path)

        # If Hugging Face API request fails, return an error response
        if status_code != 200:
            raise HTTPException(status_code=status_code, detail="Hugging Face API Error")

        return {"status_code": status_code, "violating_call_ids": violating_calls}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))