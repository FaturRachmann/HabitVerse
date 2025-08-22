# app/api/challenges.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Challenges"])
def challenges_root():
    """Basic endpoint to verify Challenges API is wired up."""
    return {"status": "ok", "message": "Challenges API"}