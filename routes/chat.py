from fastapi import APIRouter, HTTPException

from agents.ai_agent import MentalWellnessAgent
from models.schemas import ChatRequest, ChatResponse
from services.config import settings
from services.mood_context import MoodContextService
from routes.mood import mood_db  # Import the in-memory mood storage

router = APIRouter()

# Instantiate a mocked agent for now; can be swapped with OpenAI/Groq later
agent = MentalWellnessAgent(provider=settings.MODEL_PROVIDER, model=settings.MODEL_NAME)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Get mood context if user_id is provided
    mood_context = None
    if request.user_id:
        # Filter mood entries for this user
        user_moods = [mood for mood in mood_db if mood.user_id == request.user_id]
        if user_moods:
            # Sort by timestamp to get most recent first
            user_moods.sort(key=lambda x: x.timestamp)
            mood_context = MoodContextService.get_mood_context(user_moods)

    # Generate mood-aware response
    reply = agent.generate_response(
        message=request.message, 
        user_id=request.user_id,
        mood_context=mood_context
    )
    
    return ChatResponse(
        reply=reply,
        provider=agent.provider,
        model=agent.model,
    )
