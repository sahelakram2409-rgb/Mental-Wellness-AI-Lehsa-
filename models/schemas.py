from typing import Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    provider: str
    model: str
