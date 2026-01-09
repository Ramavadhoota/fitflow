# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from api import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}


def test_register_user(client):
    user_data = {
        "user_id": "test_user_123",
        "name": "Test User",
        "age": 28,
        "weight_kg": 70.0,
        "height_cm": 175,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["dumbbells", "barbell"],
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["user_id"] == "test_user_123"
    assert data["name"] == "Test User"


def test_get_profile(client):
    # First register user
    client.post("/api/v1/auth/register", json={
        "user_id": "test_user_profile",
        "name": "Profile Test",
        "age": 30,
        "weight_kg": 75.0,
        "height_cm": 180,
        "fitness_level": "advanced",
        "goal": "fat_loss",
        "equipment": ["full_gym"],
    })
    
    response = client.get("/api/v1/auth/profile?user_id=test_user_profile")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_profile"


def test_log_metrics(client):
    # Register user first
    client.post("/api/v1/auth/register", json={
        "user_id": "metrics_user",
        "name": "Metrics User",
        "age": 25,
        "weight_kg": 68.0,
        "height_cm": 170,
        "fitness_level": "beginner",
        "goal": "muscle_gain",
        "equipment": ["dumbbells"],
    })
    
    metrics_data = {
        "user_id": "metrics_user",
        "weight_kg": 68.5,
        "strength_1rm": 120.0,
        "sleep_hours": 7.2,
        "mood": 8,
        "energy": 7,
    }
    response = client.post("/api/v1/users/metrics/log", json=metrics_data)
    assert response.status_code in [200, 201]
    assert response.json()["status"] == "success"


def test_generate_plan(client):
    client.post("/api/v1/auth/register", json={
        "user_id": "plan_user",
        "name": "Plan User",
        "age": 28,
        "weight_kg": 72.0,
        "height_cm": 178,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["dumbbells", "bench"],
    })
    
    response = client.post("/api/v1/plans/generate", json={"user_id": "plan_user", "week": 1})
    assert response.status_code in [200, 201]
    data = response.json()
    assert "plan_id" in data
    assert data["user_id"] == "plan_user"


def test_chat_flow(client):
    client.post("/api/v1/auth/register", json={
        "user_id": "chat_user",
        "name": "Chat User",
        "age": 27,
        "weight_kg": 70.0,
        "height_cm": 175,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["barbell"],
    })
    
    chat_data = {"user_id": "chat_user", "message": "Help me with deadlift form"}
    response = client.post("/api/v1/chat/message", json=chat_data)
    assert response.status_code in [200, 201]
