from fastapi import APIRouter, HTTPException
from app.models.profanity import ProfanityRequest, ProfanityResponse
from app.services.profanity_regex import detect_profanity_regex
from app.services.profanity_ml import detect_profanity_ml
from app.services.profanity_llm import detect_profanity_llm

router = APIRouter()

@router.post("/detect/profanity/regex", response_model=ProfanityResponse)
def detect_profanity_using_regex(request: ProfanityRequest):
    detected_words = detect_profanity_regex(request.text)
    return {"is_profane": bool(detected_words), "detected_words": detected_words}

@router.post("/detect/profanity/ml", response_model=ProfanityResponse)
def detect_profanity_using_ml(request: ProfanityRequest):
    try:
        is_profane = detect_profanity_ml(request.text)
        return is_profane
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
    llm_result = detect_profanity_llm(request.text)
    
    return {
        "regex": {"is_profane": bool(regex_result), "detected_words": regex_result},
        "ml": {"is_profane": ml_result},
        "llm": {"is_profane": llm_result}
    }


'''

'''