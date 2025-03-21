from fastapi import FastAPI
from app.api.v1.endpoints import profanity

app = FastAPI(title="Debt Collection Call Analysis API")

# Include profanity detection endpoints
app.include_router(profanity.router, prefix="/api/v1", tags=["Profanity Detection"])

@app.get("/")
def root():
    return {"message": "Debt Collection Call Analysis API is running!"}