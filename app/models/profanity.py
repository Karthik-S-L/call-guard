from pydantic import BaseModel
from typing import List,Any

class ProfanityRequest(BaseModel):
    text: str

class ProfanityResponse(BaseModel):
    is_profane: Any
    detected_words: List[str]
