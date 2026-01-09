# tests/test_agents.py
from datetime import datetime

from agents.workout_agent import WorkoutAgent
from agents.diet_agent import DietAgent
from agents.progress_agent import ProgressAgent
from agents.coaching_agent import CoachingAgent
from agents.orchestrator import OrchestratorAgent


def _sample_user_profile():
    return {
        "user_id": "alice",
        "age": 28,
        "weight_kg": 65,
        "height_cm": 165,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["dumbbells", "barbell", "bench"],
    }


def _sample_metrics_history():
    return [
        {
            "timestamp": datetime.utcnow().isoformat(),
            "weight_kg": 65.0,
            "strength_1rm": 180.0,
            "sleep_hours": 7.5,
            "mood": 8,
            "energy": 8,
        },
        {
            "timestamp": datetime.utcnow().isoformat(),
            "weight_kg": 65.3,
            "strength_1rm": 182.5,
            "sleep_hours": 7.0,
            "mood": 7,
            "energy": 7,
        },
    ]


def test_workout_agent_generates_days():
    agent = WorkoutAgent()
    plan = agent.generate_workout_plan(
        user_profile=_sample_user_profile(),
        week=1,
        metrics_history=_sample_metrics_history(),
    )

    assert isinstance(plan, dict)
    assert "days" in plan
    assert isinstance(plan["days"], list)
    assert len(plan["days"]) >= 3
    assert all("name" in d and "exercises" in d for d in plan["days"])


def test_diet_agent_returns_macros():
    agent = DietAgent()
    plan = agent.generate_nutrition_plan(
        user_profile=_sample_user_profile(),
        metrics_history=_sample_metrics_history(),
    )

    assert isinstance(plan, dict)
    assert "calories" in plan
    assert "macros" in plan
    macros = plan["macros"]
    for key in ("protein_g", "carbs_g", "fat_g"):
        assert key in macros
        assert macros[key] > 0


def test_progress_agent_trends_and_prediction():
    agent = ProgressAgent()
    result = agent.analyze_progress(
        user_profile=_sample_user_profile(),
        metrics_history=_sample_metrics_history(),
    )

    assert isinstance(result, dict)
    assert "trends" in result
    assert "prediction_4_weeks" in result
    assert "recovery_score" in result


def test_coaching_agent_outputs_strategy():
    agent = CoachingAgent()
    result = agent.generate_coaching_strategy(
        user_profile=_sample_user_profile(),
        metrics_history=_sample_metrics_history(),
    )

    assert isinstance(result, dict)
    for key in ("strategy", "barriers", "habits", "touchpoints"):
        assert key in result


def test_orchestrator_combines_all_components():
    orchestrator = OrchestratorAgent()
    plan = orchestrator.synthesize_recommendation(
        user_profile=_sample_user_profile(),
        metrics_history=_sample_metrics_history(),
        week=1,
    )

    assert isinstance(plan, dict)
    for key in ("workout_plan", "nutrition_plan", "progress_analysis", "coaching_plan"):
        assert key in plan
    assert "summary" in plan
    assert "success_probability" in plan
