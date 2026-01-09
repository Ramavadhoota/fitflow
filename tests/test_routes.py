# tests/test_routes.py
import uuid


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"


def test_register_and_get_profile(client):
    user_payload = {
        "user_id": "alice",
        "name": "Alice Smith",
        "age": 28,
        "weight_kg": 65.0,
        "height_cm": 165,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["dumbbells", "barbell"],
    }
    r = client.post("/api/v1/auth/register", json=user_payload)
    assert r.status_code in (200, 201)
    profile = r.json()
    assert profile["user_id"] == "alice"

    r2 = client.get("/api/v1/auth/profile", params={"user_id": "alice"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["user_id"] == "alice"


def test_log_metrics_and_get_latest(client):
    # Ensure user exists
    client.post(
        "/api/v1/auth/register",
        json={
            "user_id": "alice",
            "name": "Alice",
            "age": 28,
            "weight_kg": 65.0,
            "height_cm": 165,
            "fitness_level": "intermediate",
            "goal": "muscle_gain",
            "equipment": ["dumbbells"],
        },
    )

    metric_payload = {
        "user_id": "alice",
        "weight_kg": 65.3,
        "strength_1rm": 180.0,
        "sleep_hours": 7.5,
        "mood": 8,
        "energy": 8,
    }
    r = client.post("/api/v1/users/metrics/log", json=metric_payload)
    assert r.status_code in (200, 201)

    r2 = client.get("/api/v1/users/metrics/latest", params={"user_id": "alice"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["weight_kg"] == 65.3


def test_generate_plan_and_get_current(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "user_id": "alice",
            "name": "Alice",
            "age": 28,
            "weight_kg": 65.0,
            "height_cm": 165,
            "fitness_level": "intermediate",
            "goal": "muscle_gain",
            "equipment": ["dumbbells"],
        },
    )

    r = client.post(
        "/api/v1/plans/generate",
        json={"user_id": "alice", "week": 1},
    )
    assert r.status_code in (200, 201)
    plan = r.json()
    assert "plan_id" in plan

    r2 = client.get("/api/v1/plans/current", params={"user_id": "alice"})
    assert r2.status_code == 200
    current = r2.json()
    assert current["user_id"] == "alice"


def test_chat_history_flow(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "user_id": "alice",
            "name": "Alice",
            "age": 28,
            "weight_kg": 65.0,
            "height_cm": 165,
            "fitness_level": "intermediate",
            "goal": "muscle_gain",
            "equipment": ["dumbbells"],
        },
    )

    msg_payload = {
        "user_id": "alice",
        "message": "How do I improve my bench press?",
    }
    r = client.post("/api/v1/chat/message", json=msg_payload)
    assert r.status_code in (200, 201)

    r2 = client.get("/api/v1/chat/history", params={"user_id": "alice"})
    assert r2.status_code == 200
    history = r2.json()
    assert isinstance(history, list)
    assert len(history) >= 1

    r3 = client.delete("/api/v1/chat/history", params={"user_id": "alice"})
    assert r3.status_code == 200
