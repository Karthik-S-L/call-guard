from fastapi import FastAPI
from app.api.v1.endpoints import profanity
from app.api.v1.endpoints import compliance

app = FastAPI(title="Debt Collection Call Analysis API")

# Include profanity detection endpoints
app.include_router(profanity.router, prefix="/api/v1", tags=["Profanity Detection"])
app.include_router(compliance.router, prefix="/api/v1", tags=["Compliance Detection"])

@app.get("/")
def root():
    return {"message": "Debt Collection Call Analysis API is running!"}