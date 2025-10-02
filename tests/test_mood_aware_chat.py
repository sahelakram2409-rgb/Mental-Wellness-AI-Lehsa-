from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app import app

client = TestClient(app)


def test_chat_without_mood_context():
    """Test chat response when no mood context is available."""
    response = client.post(
        "/api/chat",
        json={"message": "I'm feeling stressed about work", "user_id": "new_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "I hear you saying" in data["reply"]
    assert "general wellness suggestions" in data["reply"]
    assert "not a substitute for professional" in data["reply"]


def test_chat_with_positive_mood_context():
    """Test chat response when user has positive mood history."""
    # First, log some positive moods
    client.post("/api/mood", json={"mood_level": 8, "notes": "Great day!", "user_id": "happy_user"})
    client.post("/api/mood", json={"mood_level": 9, "notes": "Feeling awesome", "user_id": "happy_user"})
    
    # Now chat
    response = client.post(
        "/api/chat",
        json={"message": "I want to keep feeling this good", "user_id": "happy_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "wonderful that you're feeling so positive" in data["reply"]
    assert "mood level 9/10" in data["reply"]
    assert "maintain this great energy" in data["reply"]
    assert "recently noted: \"Feeling awesome\"" in data["reply"]


def test_chat_with_low_mood_context():
    """Test chat response when user has low mood history."""
    # Log some low moods
    client.post("/api/mood", json={"mood_level": 2, "notes": "Really struggling", "user_id": "struggling_user"})
    client.post("/api/mood", json={"mood_level": 3, "notes": "Still tough", "user_id": "struggling_user"})
    
    # Chat
    response = client.post(
        "/api/chat",
        json={"message": "Everything feels overwhelming", "user_id": "struggling_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "really sorry you're struggling" in data["reply"]
    assert "mood level 3/10" in data["reply"]
    assert "immediate steps" in data["reply"]
    assert "recently noted: \"Still tough\"" in data["reply"]
    assert "professional support" in data["reply"]


def test_chat_with_improving_mood_trend():
    """Test chat response when user's mood is improving."""
    # Log moods showing improvement
    base_time = datetime.utcnow()
    client.post("/api/mood", json={
        "mood_level": 3, 
        "notes": "Starting low", 
        "user_id": "improving_user"
    })
    client.post("/api/mood", json={
        "mood_level": 5, 
        "notes": "Getting better", 
        "user_id": "improving_user"
    })
    client.post("/api/mood", json={
        "mood_level": 7, 
        "notes": "Much better now", 
        "user_id": "improving_user"
    })
    
    # Chat
    response = client.post(
        "/api/chat",
        json={"message": "I think I'm doing better", "user_id": "improving_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "mood has been improving recently" in data["reply"]
    assert "positive momentum" in data["reply"]
    assert "mood level 7/10" in data["reply"]


def test_chat_with_declining_mood_trend():
    """Test chat response when user's mood is declining."""
    # Log moods showing decline
    client.post("/api/mood", json={
        "mood_level": 8, 
        "notes": "Was feeling good", 
        "user_id": "declining_user"
    })
    client.post("/api/mood", json={
        "mood_level": 5, 
        "notes": "Getting harder", 
        "user_id": "declining_user"
    })
    client.post("/api/mood", json={
        "mood_level": 3, 
        "notes": "Really down now", 
        "user_id": "declining_user"
    })
    
    # Chat
    response = client.post(
        "/api/chat",
        json={"message": "Things are getting worse", "user_id": "declining_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "mood has been declining lately" in data["reply"]
    assert "extra gentle with yourself" in data["reply"]
    assert "additional support" in data["reply"]
    assert "mood level 3/10" in data["reply"]


def test_chat_neutral_mood_context():
    """Test chat response for neutral mood range."""
    # Log neutral moods
    client.post("/api/mood", json={"mood_level": 5, "notes": "Just okay", "user_id": "neutral_user"})
    client.post("/api/mood", json={"mood_level": 4, "notes": "Meh", "user_id": "neutral_user"})
    
    # Chat
    response = client.post(
        "/api/chat",
        json={"message": "I'm feeling pretty average", "user_id": "neutral_user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "balanced state" in data["reply"]
    assert "mood level 4/10" in data["reply"]
    assert "gentle suggestions" in data["reply"]


def test_chat_without_user_id():
    """Test chat response when no user_id is provided (no mood context)."""
    response = client.post(
        "/api/chat",
        json={"message": "I need some help"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "I hear you saying" in data["reply"]
    assert "general wellness suggestions" in data["reply"]
    # Should not include mood-specific language
    assert "mood level" not in data["reply"]


def test_chat_empty_message_still_fails():
    """Test that empty messages still return validation error."""
    response = client.post(
        "/api/chat",
        json={"message": "", "user_id": "test_user"}
    )
    assert response.status_code == 422  # Pydantic validation error
    assert "String should have at least 1 character" in str(response.json())


def test_mood_context_service_directly():
    """Test the mood context service functionality directly."""
    from services.mood_context import MoodContextService
    from models.schemas import MoodEntry
    from datetime import datetime
    
    # Test with no moods
    context = MoodContextService.get_mood_context([])
    assert context["status"] == "no_data"
    
    # Test with moods
    moods = [
        MoodEntry(user_id="test", mood_level=3, notes="low", timestamp=datetime.utcnow() - timedelta(days=2)),
        MoodEntry(user_id="test", mood_level=7, notes="better", timestamp=datetime.utcnow())
    ]
    
    context = MoodContextService.get_mood_context(moods)
    assert context["status"] == "available"
    assert context["latest_mood"] == 7
    assert context["trend"] == "improving"
    assert context["category"] == "positive"


def test_full_mood_aware_workflow():
    """Test the complete workflow: log moods, then chat."""
    user_id = "workflow_user"
    
    # Step 1: Log some moods over time
    client.post("/api/mood", json={
        "mood_level": 4, 
        "notes": "Starting point", 
        "user_id": user_id
    })
    client.post("/api/mood", json={
        "mood_level": 6, 
        "notes": "Getting better", 
        "user_id": user_id
    })
    client.post("/api/mood", json={
        "mood_level": 8, 
        "notes": "Feeling great!", 
        "user_id": user_id
    })
    
    # Step 2: Verify mood history
    mood_response = client.get(f"/api/mood/history?user_id={user_id}")
    assert mood_response.status_code == 200
    mood_data = mood_response.json()
    assert len(mood_data["moods"]) >= 3
    
    # Step 3: Chat and get mood-aware response
    chat_response = client.post(
        "/api/chat",
        json={
            "message": "I want to talk about how I've been feeling", 
            "user_id": user_id
        }
    )
    assert chat_response.status_code == 200
    chat_data = chat_response.json()
    
    # Verify mood awareness in response
    assert "mood level 8/10" in chat_data["reply"]
    assert "improving recently" in chat_data["reply"]
    assert "Feeling great!" in chat_data["reply"]
    assert "positive" in chat_data["reply"]