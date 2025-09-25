from typing import Optional


class MentalWellnessAgent:
    """Mocked AI agent for mental wellness interactions.

    Replace internals with real provider (OpenAI/Groq) when ready.
    """

    def __init__(self, provider: str = "mock", model: str = "mock-model"):
        self.provider = provider
        self.model = model

    def generate_response(self, message: str, user_id: Optional[str] = None) -> str:
        """Return a deterministic, safe placeholder response."""
        canned = (
            "Thanks for sharing. While I'm not a substitute for professional help, "
            "here are some general tips:\n"
            "- Take a few deep, slow breaths.\n"
            "- Consider a short walk or gentle stretch.\n"
            "- Write down how you’re feeling.\n"
            "If you’re in crisis, please contact your local emergency number."
        )
        msg = message.strip() if message else ""
        if msg:
            return f'I hear you saying: "{msg}".' "\n\n" + canned
        return canned
