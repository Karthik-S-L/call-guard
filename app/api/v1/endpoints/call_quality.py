import os
from fastapi import APIRouter, HTTPException
from app.services.call_quality import calculate_overtalk_and_silence

router = APIRouter()
FOLDER_PATH = "yaml-sample-folder/All_Conversations/"

@router.get("/call-quality", response_model=dict)
def get_call_quality_metrics():
    """
    Calculates call quality metrics including overtalk and silence duration.

    Returns:
    --------
    dict:
        {
            "status_code": 200 if successful, otherwise an error code,
            "call_quality_metrics": {
                "overtalk_percentage": float,
                "silence_percentage": float,
                ...
            }
        }
    """
    try:
        if not os.path.exists(FOLDER_PATH):
            raise HTTPException(status_code=404, detail="Folder not found")

        results = calculate_overtalk_and_silence(FOLDER_PATH)

        if not isinstance(results, dict):
            raise HTTPException(status_code=500, detail="Invalid response from call quality function")

        return {"status_code": 200, "call_quality_metrics": results}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Error accessing the folder.")
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=f"Invalid data format: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
