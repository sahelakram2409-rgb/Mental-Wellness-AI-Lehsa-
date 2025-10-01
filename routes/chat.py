from fastapi import APIRouter, HTTPException

from agents.ai_agent import MentalWellnessAgent
from models.schemas import ChatRequest, ChatResponse
from services.config import settings

router = APIRouter()

# Instantiate a mocked agent for now; can be swapped with OpenAI/Groq later
agent = MentalWellnessAgent(provider=settings.MODEL_PROVIDER, model=settings.MODEL_NAME)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    reply = agent.generate_response(request.message, user_id=request.user_id)
    return ChatResponse(
        reply=reply,
        provider=agent.provider,
        model=agent.model,
    )
