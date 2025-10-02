from typing import Optional, Dict, Any


class MentalWellnessAgent:
    """AI agent for mental wellness interactions with mood-aware responses.

    Replace internals with real provider (OpenAI/Groq) when ready.
    """

    def __init__(self, provider: str = "mock", model: str = "mock-model"):
        self.provider = provider
        self.model = model

    def generate_response(self, message: str, user_id: Optional[str] = None, mood_context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a mood-aware response based on user message and mood context."""
        msg = message.strip() if message else ""
        
        if not msg:
            return self._get_default_response()
        
        if mood_context and mood_context.get("status") == "available":
            return self._generate_mood_aware_response(msg, mood_context)
        else:
            return self._generate_basic_response(msg)

    def _generate_mood_aware_response(self, message: str, mood_context: Dict[str, Any]) -> str:
        """Generate response tailored to user's mood state."""
        category = mood_context.get("category", "neutral")
        trend = mood_context.get("trend", "stable")
        latest_mood = mood_context.get("latest_mood", 5)
        latest_notes = mood_context.get("latest_notes")
        
        # Acknowledge the user's message
        acknowledgment = f'I hear you saying: "{message}".'
        
        # Add mood-specific context if we have recent notes
        if latest_notes:
            acknowledgment += f' I also notice you recently noted: "{latest_notes}".'
        
        # Generate mood-appropriate response
        mood_response = self._get_mood_specific_response(category, trend, latest_mood)
        
        # Add trend-specific encouragement
        trend_response = self._get_trend_response(trend)
        
        return f"{acknowledgment}\n\n{mood_response}{trend_response}\n\n{self._get_safety_disclaimer()}"

    def _get_mood_specific_response(self, category: str, trend: str, latest_mood: int) -> str:
        """Get response based on mood category."""
        responses = {
            "very_positive": (
                f"It's wonderful that you're feeling so positive (mood level {latest_mood}/10)! "
                "Here are ways to maintain this great energy:\n"
                "- Share your positivity with others\n"
                "- Engage in activities you love\n"
                "- Practice gratitude for this good feeling\n"
                "- Use this energy for personal goals"
            ),
            "positive": (
                f"I'm glad to see you're in a good space (mood level {latest_mood}/10). "
                "Here are some suggestions to nurture this positive state:\n"
                "- Take time to appreciate what's going well\n"
                "- Connect with supportive people\n"
                "- Engage in activities that bring you joy\n"
                "- Consider helping others, which can boost mood further"
            ),
            "neutral": (
                f"I understand you're in a balanced state (mood level {latest_mood}/10). "
                "Here are some gentle suggestions for well-being:\n"
                "- Take a few mindful breaths\n"
                "- Go for a short walk in nature if possible\n"
                "- Do something small that usually brings you comfort\n"
                "- Check in with yourself about what you might need today"
            ),
            "low": (
                f"I can see you're having a tough time (mood level {latest_mood}/10), and that's completely valid. "
                "Here are some gentle strategies that might help:\n"
                "- Practice slow, deep breathing for a few minutes\n"
                "- Try a short walk or gentle movement\n"
                "- Reach out to someone you trust\n"
                "- Be kind to yourself - difficult feelings are temporary"
            ),
            "very_low": (
                f"I'm really sorry you're struggling so much right now (mood level {latest_mood}/10). "
                "Your feelings are valid, and you don't have to face this alone. Here are some immediate steps:\n"
                "- Focus on slow, deep breathing\n"
                "- Try to stay in the present moment\n"
                "- Reach out to a trusted friend, family member, or counselor\n"
                "- Consider professional support if you haven't already"
            )
        }
        
        return responses.get(category, self._get_default_response())

    def _get_trend_response(self, trend: str) -> str:
        """Add trend-specific encouragement."""
        trend_responses = {
            "improving": "\n\nI'm encouraged to see your mood has been improving recently. Keep up the positive momentum!",
            "declining": "\n\nI notice your mood has been declining lately. This is a good time to be extra gentle with yourself and consider additional support.",
            "stable": "\n\nYour mood has been fairly consistent recently, which shows good stability."
        }
        
        return trend_responses.get(trend, "")

    def _generate_basic_response(self, message: str) -> str:
        """Generate basic response when no mood context is available."""
        acknowledgment = f'I hear you saying: "{message}".'
        
        basic_tips = (
            "Here are some general wellness suggestions:\n"
            "- Take a few deep, slow breaths\n"
            "- Consider a short walk or gentle stretch\n"
            "- Write down how you're feeling\n"
            "- Connect with someone you trust"
        )
        
        return f"{acknowledgment}\n\n{basic_tips}\n\n{self._get_safety_disclaimer()}"

    def _get_default_response(self) -> str:
        """Default response when no message is provided."""
        return (
            "Hello! I'm here to support your mental wellness journey. "
            "Feel free to share what's on your mind, and I'll do my best to provide helpful guidance.\n\n"
            f"{self._get_safety_disclaimer()}"
        )

    def _get_safety_disclaimer(self) -> str:
        """Safety disclaimer for all responses."""
        return (
            "Remember: I'm not a substitute for professional mental health care. "
            "If you're in crisis or need immediate help, please contact your local emergency services "
            "or a mental health crisis line."
        )
