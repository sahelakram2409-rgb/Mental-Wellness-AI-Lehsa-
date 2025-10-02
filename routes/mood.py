from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from models.schemas import MoodEntry, MoodResponse
from services.database import get_db
from services.repositories import MoodRepository, convert_mood_entry_to_schema

router = APIRouter()


@router.post("/mood", response_model=MoodEntry)
async def log_mood(entry: MoodEntry, db: Session = Depends(get_db)):
    """Log a mood entry for a user."""
    mood_repo = MoodRepository(db)
    
    # Use a default user_id if none provided (for backward compatibility)
    user_id = entry.user_id or "anonymous_user"
    
    # Create mood entry in database
    db_mood = mood_repo.create_mood_entry(
        user_id=user_id,
        mood_level=entry.mood_level,
        notes=entry.notes,
        timestamp=entry.timestamp
    )
    
    # Convert to schema and return
    return convert_mood_entry_to_schema(db_mood)


@router.get("/mood/history", response_model=MoodResponse)
async def get_mood_history(user_id: Optional[str] = None, days_back: int = 7, db: Session = Depends(get_db)):
    """Get mood history for a specific user or all users."""
    mood_repo = MoodRepository(db)
    
    if user_id:
        # Get moods for specific user
        db_moods = mood_repo.get_mood_entries_by_user(user_id, days_back=days_back)
        mood_schemas = [convert_mood_entry_to_schema(mood) for mood in db_moods]
        return MoodResponse(user_id=user_id, moods=mood_schemas)
    else:
        # For backward compatibility, return anonymous_user data if no user_id provided
        db_moods = mood_repo.get_mood_entries_by_user("anonymous_user", days_back=days_back)
        mood_schemas = [convert_mood_entry_to_schema(mood) for mood in db_moods]
        return MoodResponse(user_id=None, moods=mood_schemas)


@router.get("/mood/statistics")
async def get_mood_statistics(user_id: str, days_back: int = 30, db: Session = Depends(get_db)):
    """Get mood statistics for a user."""
    mood_repo = MoodRepository(db)
    
    stats = mood_repo.get_user_mood_statistics(user_id, days_back)
    return {
        "user_id": user_id,
        "statistics": stats
    }
