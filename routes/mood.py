from fastapi import APIRouter
from models.schemas import MoodEntry, MoodResponse
from typing import List

router = APIRouter()
mood_db: List[MoodEntry] = []  # Temporary in-memory storage


@router.post("/mood", response_model=MoodEntry)
async def log_mood(entry: MoodEntry):
    """Log a mood entry for a user."""
    mood_db.append(entry)
    return entry


@router.get("/mood/history", response_model=MoodResponse)
async def get_mood_history(user_id: str = None):
    """Get mood history for a specific user or all users."""
    if user_id:
        filtered = [m for m in mood_db if m.user_id == user_id]
    else:
        filtered = mood_db
    return MoodResponse(user_id=user_id, moods=filtered)