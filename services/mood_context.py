from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from models.schemas import MoodEntry


class MoodContextService:
    """Service for analyzing mood patterns and providing context for AI responses."""

    @staticmethod
    def get_mood_context(user_moods: List[MoodEntry], days_back: int = 7) -> Dict[str, Any]:
        """Analyze recent mood entries and return context for AI responses."""
        if not user_moods:
            return {"status": "no_data", "message": "No mood history available"}

        # Filter to recent moods (last N days)
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        recent_moods = [
            mood for mood in user_moods 
            if mood.timestamp >= cutoff_date
        ]

        if not recent_moods:
            return {"status": "no_recent_data", "message": "No recent mood data available"}

        # Calculate mood statistics
        mood_levels = [mood.mood_level for mood in recent_moods]
        avg_mood = sum(mood_levels) / len(mood_levels)
        latest_mood = recent_moods[-1].mood_level
        trend = MoodContextService._calculate_trend(recent_moods)

        # Determine mood category
        mood_category = MoodContextService._categorize_mood(avg_mood, latest_mood)

        return {
            "status": "available",
            "average_mood": round(avg_mood, 1),
            "latest_mood": latest_mood,
            "trend": trend,
            "category": mood_category,
            "entry_count": len(recent_moods),
            "days_analyzed": days_back,
            "latest_notes": recent_moods[-1].notes if recent_moods[-1].notes else None
        }

    @staticmethod
    def _calculate_trend(moods: List[MoodEntry]) -> str:
        """Calculate mood trend (improving, declining, stable)."""
        if len(moods) < 2:
            return "insufficient_data"

        # Compare first half vs second half of mood entries
        mid_point = len(moods) // 2
        first_half_avg = sum(mood.mood_level for mood in moods[:mid_point]) / mid_point
        second_half_avg = sum(mood.mood_level for mood in moods[mid_point:]) / (len(moods) - mid_point)

        diff = second_half_avg - first_half_avg

        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        else:
            return "stable"

    @staticmethod
    def _categorize_mood(avg_mood: float, latest_mood: int) -> str:
        """Categorize overall mood state."""
        # Prioritize latest mood but consider average
        primary_score = latest_mood * 0.7 + avg_mood * 0.3

        if primary_score >= 8:
            return "very_positive"
        elif primary_score >= 6:
            return "positive"
        elif primary_score >= 4:
            return "neutral"
        elif primary_score >= 3:
            return "low"
        else:
            return "very_low"

    @staticmethod
    def generate_mood_aware_prompt(context: Dict[str, Any], user_message: str) -> str:
        """Generate a context-aware prompt for the AI based on mood analysis."""
        if context["status"] != "available":
            return f"User message: {user_message}"

        category = context["category"]
        trend = context["trend"]
        latest_mood = context["latest_mood"]
        latest_notes = context.get("latest_notes")

        # Build context prompt
        mood_context = f"User's recent mood context:\n"
        mood_context += f"- Current mood level: {latest_mood}/10\n"
        mood_context += f"- Recent average: {context['average_mood']}/10\n"
        mood_context += f"- Trend: {trend}\n"
        mood_context += f"- Overall state: {category}\n"
        
        if latest_notes:
            mood_context += f"- Latest notes: '{latest_notes}'\n"

        # Add guidance for response tone
        response_guidance = MoodContextService._get_response_guidance(category, trend)
        
        return f"{mood_context}\n{response_guidance}\n\nUser message: {user_message}"

    @staticmethod
    def _get_response_guidance(category: str, trend: str) -> str:
        """Get guidance for AI response tone based on mood category and trend."""
        guidance_map = {
            "very_positive": "User is feeling very positive. Be encouraging and help maintain this positive state. Suggest ways to sustain good mental health.",
            "positive": "User is in a good mood. Be supportive and positive. Share tips for maintaining well-being.",
            "neutral": "User has a neutral mood. Be gently encouraging and offer practical wellness suggestions.",
            "low": "User is experiencing low mood. Be extra compassionate and supportive. Offer gentle, practical suggestions and validate their feelings.",
            "very_low": "User is experiencing very low mood. Be very gentle, compassionate, and supportive. Focus on immediate coping strategies and emphasize professional help if needed."
        }

        base_guidance = guidance_map.get(category, "Be supportive and helpful.")

        if trend == "declining":
            base_guidance += " Note that their mood has been declining recently - be extra gentle and offer specific coping strategies."
        elif trend == "improving":
            base_guidance += " Their mood has been improving recently - acknowledge this positive trend."

        return f"Response guidance: {base_guidance}"