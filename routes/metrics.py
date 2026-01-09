from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.entities import User, Metric, get_db
from models.schemas import MetricLog, SuccessResponse

router = APIRouter(
    prefix="/api/v1/users/metrics",
    tags=["Metrics"],
    responses={404: {"description": "Not found"}}
)


@router.post("/log", response_model=SuccessResponse)
def log_metrics(
    metric_data: MetricLog,
    db: Session = Depends(get_db)
):
    """
    Log user metrics
    
    Records weight, strength (1RM), sleep hours, mood, and energy level.
    Used for progress tracking and trend analysis.
    
    Example request:
    ```json
    {
        "user_id": "alice",
        "weight_kg": 65.5,
        "strength_1rm": 185,
        "sleep_hours": 7.5,
        "mood": 8,
        "energy": 8
    }
    ```
    
    All fields are required:
    - weight_kg: Body weight in kilograms
    - strength_1rm: Maximum strength (1 rep max) in kg
    - sleep_hours: Hours of sleep (0-24)
    - mood: Mood score (1-10)
    - energy: Energy level (1-10)
    
    Response:
    ```json
    {
        "status": "success",
        "message": "Metrics logged successfully"
    }
    ```
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == metric_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{metric_data.user_id}' not found"
        )
    
    # Validate metric values
    if metric_data.weight_kg < 30 or metric_data.weight_kg > 300:
        raise HTTPException(
            status_code=400,
            detail="Weight must be between 30 and 300 kg"
        )
    
    if metric_data.strength_1rm < 0 or metric_data.strength_1rm > 500:
        raise HTTPException(
            status_code=400,
            detail="Strength (1RM) must be between 0 and 500 kg"
        )
    
    if metric_data.sleep_hours < 0 or metric_data.sleep_hours > 24:
        raise HTTPException(
            status_code=400,
            detail="Sleep hours must be between 0 and 24"
        )
    
    if metric_data.mood < 1 or metric_data.mood > 10:
        raise HTTPException(
            status_code=400,
            detail="Mood must be between 1 and 10"
        )
    
    if metric_data.energy < 1 or metric_data.energy > 10:
        raise HTTPException(
            status_code=400,
            detail="Energy must be between 1 and 10"
        )
    
    # Create metric record
    db_metric = Metric(
        user_id=metric_data.user_id,
        weight_kg=metric_data.weight_kg,
        strength_1rm=metric_data.strength_1rm,
        sleep_hours=metric_data.sleep_hours,
        mood=metric_data.mood,
        energy=metric_data.energy
    )
    
    db.add(db_metric)
    db.commit()
    
    return {
        "status": "success",
        "message": "Metrics logged successfully"
    }


@router.get("")
def get_metrics(
    user_id: str,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """
    Get all metrics for a user
    
    Retrieves complete metrics history in chronological order.
    
    Query parameters:
    - user_id: The user ID
    - limit: Maximum number of records to return (optional)
    
    Example request:
    ```
    GET /api/v1/users/metrics?user_id=alice&limit=30
    ```
    
    Response:
    ```json
    {
        "status": "success",
        "count": 5,
        "metrics": [
            {
                "weight_kg": 65.0,
                "strength_1rm": 180,
                "sleep_hours": 7.5,
                "mood": 8,
                "energy": 7,
                "created_at": "2026-01-01T10:00:00"
            },
            ...
        ]
    }
    ```
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    # Get metrics
    query = db.query(Metric).filter(
        Metric.user_id == user_id
    ).order_by(Metric.created_at)
    
    if limit:
        query = query.limit(limit)
    
    metrics = query.all()
    
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for user '{user_id}'"
        )
    
    return {
        "status": "success",
        "count": len(metrics),
        "metrics": [
            {
                "weight_kg": m.weight_kg,
                "strength_1rm": m.strength_1rm,
                "sleep_hours": m.sleep_hours,
                "mood": m.mood,
                "energy": m.energy,
                "created_at": m.created_at.isoformat()
            }
            for m in metrics
        ]
    }


@router.get("/latest")
def get_latest_metrics(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the most recent metrics for a user
    
    Returns only the latest metric entry.
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    metric = db.query(Metric).filter(
        Metric.user_id == user_id
    ).order_by(Metric.created_at.desc()).first()
    
    if not metric:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for user '{user_id}'"
        )
    
    return {
        "status": "success",
        "latest": {
            "weight_kg": metric.weight_kg,
            "strength_1rm": metric.strength_1rm,
            "sleep_hours": metric.sleep_hours,
            "mood": metric.mood,
            "energy": metric.energy,
            "created_at": metric.created_at.isoformat()
        }
    }


@router.get("/trends")
def get_metric_trends(
    user_id: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get metric trends over time
    
    Analyzes trends in weight, strength, and mood over specified period.
    
    Query parameters:
    - user_id: The user ID
    - days: Number of days to analyze (default: 30)
    """
    from datetime import datetime, timedelta
    
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    metrics = db.query(Metric).filter(
        Metric.user_id == user_id,
        Metric.created_at >= cutoff_date
    ).order_by(Metric.created_at).all()
    
    if len(metrics) < 2:
        raise HTTPException(
            status_code=400,
            detail=f"Need at least 2 metrics to calculate trends (found {len(metrics)})"
        )
    
    # Calculate trends
    weight_change = metrics[-1].weight_kg - metrics.weight_kg
    strength_change = metrics[-1].strength_1rm - metrics.strength_1rm
    avg_mood = sum(m.mood for m in metrics) / len(metrics)
    avg_sleep = sum(m.sleep_hours for m in metrics) / len(metrics)
    
    return {
        "status": "success",
        "period_days": days,
        "metric_count": len(metrics),
        "trends": {
            "weight_change_kg": round(weight_change, 1),
            "strength_change_kg": round(strength_change, 1),
            "avg_mood": round(avg_mood, 1),
            "avg_sleep_hours": round(avg_sleep, 1),
            "trend_direction": "improving" if strength_change > 0 else "declining"
        }
    }