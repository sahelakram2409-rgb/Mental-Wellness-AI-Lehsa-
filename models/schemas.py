from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    provider: str
    model: str


class MoodEntry(BaseModel):
    user_id: Optional[str] = None
    mood_level: int = Field(..., ge=1, le=10, description="Mood rating from 1 to 10")
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MoodResponse(BaseModel):
    user_id: Optional[str] = None
    moods: List[MoodEntry]
