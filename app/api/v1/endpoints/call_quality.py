# app/api/v1/endpoints/call_quality.py

import os
from fastapi import APIRouter, HTTPException
from app.services.call_quality import calculate_overtalk_and_silence

router = APIRouter()

@router.get("/call-quality")
def get_call_quality_metrics():
    try:
        folder_path = "yaml-sample-folder/All_Conversations/"
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail="Folder not found")

        results = calculate_overtalk_and_silence(folder_path)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
