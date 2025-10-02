from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from agents.ai_agent import MentalWellnessAgent
from models.schemas import ChatRequest, ChatResponse
from services.config import settings
from services.mood_context import MoodContextService
from services.database import get_db
from services.repositories import MoodRepository, ChatRepository, convert_mood_entry_to_schema

router = APIRouter()

# Instantiate a mocked agent for now; can be swapped with OpenAI/Groq later
agent = MentalWellnessAgent(provider=settings.MODEL_PROVIDER, model=settings.MODEL_NAME)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Get mood context if user_id is provided
    mood_context = None
    if request.user_id:
        mood_repo = MoodRepository(db)
        # Get recent mood entries for this user
        db_moods = mood_repo.get_mood_entries_by_user(request.user_id, days_back=7)
        if db_moods:
            # Convert to schema objects for mood context service
            user_moods = [convert_mood_entry_to_schema(mood) for mood in db_moods]
            mood_context = MoodContextService.get_mood_context(user_moods)

    # Generate mood-aware response
    reply = agent.generate_response(
        message=request.message, 
        user_id=request.user_id,
        mood_context=mood_context
    )
    
    # Store chat message in database if user_id is provided
    if request.user_id:
        chat_repo = ChatRepository(db)
        chat_repo.create_chat_message(
            user_id=request.user_id,
            message=request.message,
            response=reply,
            ai_provider=agent.provider,
            ai_model=agent.model,
            mood_context=mood_context
        )
    
    return ChatResponse(
        reply=reply,
        provider=agent.provider,
        model=agent.model,
    )


@router.get("/chat/history")
async def get_chat_history(user_id: str, limit: int = 20, db: Session = Depends(get_db)):
    """Get chat history for a user."""
    chat_repo = ChatRepository(db)
    
    messages = chat_repo.get_chat_history_by_user(user_id, limit)
    
    return {
        "user_id": user_id,
        "messages": [
            {
                "id": msg.id,
                "message": msg.message,
                "response": msg.response,
                "timestamp": msg.timestamp,
                "ai_provider": msg.ai_provider,
                "ai_model": msg.ai_model
            }
            for msg in messages
        ]
    }
