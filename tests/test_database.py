# tests/test_database.py
from models.database import (
    User,
    Metric,
    Plan,
    ChatMessage,
    create_user,
    get_user,
    log_metric,
    get_user_metrics,
    save_plan,
    get_current_plan,
    save_chat_message,
    get_chat_history,
    get_db_stats,
)


def test_create_and_get_user(db_session):
    user = create_user(
        db_session,
        user_id="alice",
        name="Alice Smith",
        age=28,
        weight_kg=65.0,
        height_cm=165,
        fitness_level="intermediate",
        goal="muscle_gain",
        equipment=["dumbbells", "barbell"],
    )
    assert isinstance(user, User)
    fetched = get_user(db_session, "alice")
    assert fetched is not None
    assert fetched.user_id == "alice"


def test_log_metric_and_query(db_session):
    create_user(
        db_session,
        user_id="alice",
        name="Alice Smith",
        age=28,
        weight_kg=65.0,
        height_cm=165,
        fitness_level="intermediate",
        goal="muscle_gain",
        equipment=["dumbbells"],
    )
    metric = log_metric(
        db_session,
        user_id="alice",
        weight_kg=65.2,
        strength_1rm=180.0,
        sleep_hours=7.5,
        mood=8,
        energy=8,
    )
    assert isinstance(metric, Metric)

    metrics = get_user_metrics(db_session, "alice")
    assert len(metrics) == 1
    assert metrics[0].weight_kg == 65.2


def test_save_plan_and_get_current(db_session):
    create_user(
        db_session,
        user_id="alice",
        name="Alice Smith",
        age=28,
        weight_kg=65.0,
        height_cm=165,
        fitness_level="intermediate",
        goal="muscle_gain",
        equipment=["dumbbells"],
    )
    save_plan(
        db_session,
        plan_id="plan_test_1",
        user_id="alice",
        week=1,
        plan_data={"workout_plan": {}, "nutrition_plan": {}},
    )
    current = get_current_plan(db_session, "alice")
    assert current is not None
    assert current.plan_id == "plan_test_1"


def test_save_chat_and_get_history(db_session):
    create_user(
        db_session,
        user_id="alice",
        name="Alice Smith",
        age=28,
        weight_kg=65.0,
        height_cm=165,
        fitness_level="intermediate",
        goal="muscle_gain",
        equipment=["dumbbells"],
    )
    save_chat_message(
        db_session,
        user_id="alice",
        user_message="Hello coach",
        bot_response="Hi Alice, let's get started!",
    )
    history = get_chat_history(db_session, "alice", limit=10)
    assert len(history) == 1
    msg = history[0]
    assert isinstance(msg, ChatMessage)
    assert msg.user_message.startswith("Hello")


def test_db_stats_counts(db_session):
    # DB is per-test; just ensure stats call works
    stats = get_db_stats(db_session)
    assert {"users", "metrics", "plans", "chat_messages"} <= stats.keys()
    assert all(isinstance(v, int) for v in stats.values())
