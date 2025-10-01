from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_log_mood():
    """Test logging a mood entry."""
    response = client.post(
        "/api/mood",
        json={"mood_level": 7, "notes": "Feeling good today!", "user_id": "test_user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mood_level"] == 7
    assert data["notes"] == "Feeling good today!"
    assert data["user_id"] == "test_user"
    assert "timestamp" in data


def test_log_mood_without_notes():
    """Test logging a mood entry without notes."""
    response = client.post("/api/mood", json={"mood_level": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["mood_level"] == 5
    assert data["notes"] is None


def test_mood_level_validation():
    """Test mood level validation (should be 1-10)."""
    # Test invalid low value
    response = client.post("/api/mood", json={"mood_level": 0})
    assert response.status_code == 422

    # Test invalid high value
    response = client.post("/api/mood", json={"mood_level": 11})
    assert response.status_code == 422

    # Test valid values
    response = client.post("/api/mood", json={"mood_level": 1})
    assert response.status_code == 200

    response = client.post("/api/mood", json={"mood_level": 10})
    assert response.status_code == 200


def test_get_mood_history():
    """Test retrieving mood history."""
    # First, log a few mood entries
    client.post("/api/mood", json={"mood_level": 8, "user_id": "user1"})
    client.post("/api/mood", json={"mood_level": 6, "user_id": "user1"})
    client.post("/api/mood", json={"mood_level": 9, "user_id": "user2"})

    # Get all history
    response = client.get("/api/mood/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data["moods"]) >= 3  # At least 3 from this test

    # Get history for specific user
    response = client.get("/api/mood/history?user_id=user1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user1"
    # Should have at least 2 entries for user1
    user1_moods = [m for m in data["moods"] if m["user_id"] == "user1"]
    assert len(user1_moods) >= 2


def test_log_and_get_mood_integration():
    """Test the full flow of logging and retrieving moods."""
    # Log a mood
    log_response = client.post(
        "/api/mood", json={"mood_level": 7, "notes": "Integration test", "user_id": "integration_user"}
    )
    assert log_response.status_code == 200

    # Get history and verify it's there
    history_response = client.get("/api/mood/history?user_id=integration_user")
    assert history_response.status_code == 200
    data = history_response.json()

    # Find our logged mood
    integration_moods = [m for m in data["moods"] if m["notes"] == "Integration test"]
    assert len(integration_moods) >= 1
    assert integration_moods[0]["mood_level"] == 7