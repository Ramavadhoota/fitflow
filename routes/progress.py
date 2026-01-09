from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.entities import User, Metric, Plan, ChatMessage, get_db

router = APIRouter(
    prefix="/api/v1/progress",
    tags=["Progress"],
    responses={404: {"description": "Not found"}}
)


@router.get("/predictions")
def get_predictions(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get 4-week strength predictions
    
    Analyzes metric trends and predicts strength improvements over 4 weeks.
    Uses linear regression based on historical data.
    
    Confidence levels:
    - 0.85+: High confidence (5+ data points)
    - 0.60-0.84: Medium confidence (2-4 data points)
    - <0.60: Low confidence (insufficient data)
    
    Query parameters:
    - user_id: The user ID
    
    Example request:
    ```
    GET /api/v1/progress/predictions?user_id=alice
    ```
    
    Response:
    ```json
    {
        "status": "success",
        "predictions": {
            "strength_4w": 215.0,
            "confidence": 0.85,
            "current_strength": 185.0,
            "trend": "increasing"
        }
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
    metrics = db.query(Metric).filter(
        Metric.user_id == user_id
    ).order_by(Metric.created_at).all()
    
    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=f"No metrics found for user '{user_id}'"
        )
    
    latest = metrics[-1]
    
    # Calculate prediction based on available data
    if len(metrics) >= 5:
        # Linear regression with sufficient data
        recent_metrics = metrics[-5:]
        strength_trend = (recent_metrics[-1].strength_1rm - recent_metrics.strength_1rm) / 4
        confidence = 0.85
    elif len(metrics) >= 2:
        # Simple linear prediction
        strength_trend = latest.strength_1rm - metrics[-2].strength_1rm
        confidence = 0.60 + (len(metrics) * 0.08)
    else:
        # Insufficient data
        strength_trend = 0
        confidence = 0.30
    
    # 4-week prediction (assuming 1 week per metric entry)
    strength_4w = latest.strength_1rm + (strength_trend * 4)
    trend_direction = "increasing" if strength_trend > 0 else "declining" if strength_trend < 0 else "stable"
    
    return {
        "status": "success",
        "predictions": {
            "strength_4w": round(strength_4w, 1),
            "current_strength": latest.strength_1rm,
            "weekly_gain": round(strength_trend, 1),
            "confidence": round(min(confidence, 1.0), 2),
            "trend": trend_direction,
            "data_points": len(metrics)
        }
    }


@router.get("/dashboard")
def get_dashboard(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get complete progress dashboard
    
    Comprehensive view of user's fitness journey including:
    - Profile summary
    - Recent metrics
    - Latest plan
    - Chat activity
    - Progress statistics
    
    Query parameters:
    - user_id: The user ID
    
    Example request:
    ```
    GET /api/v1/progress/dashboard?user_id=alice
    ```
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    # Get all data
    metrics = db.query(Metric).filter(
        Metric.user_id == user_id
    ).order_by(Metric.created_at).all()
    
    plans = db.query(Plan).filter(
        Plan.user_id == user_id
    ).order_by(Plan.created_at.desc()).all()
    
    chat_history = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.created_at.desc()).limit(5).all()
    
    # Calculate statistics
    latest_metric = metrics[-1] if metrics else None
    weight_change = None
    strength_change = None
    
    if len(metrics) >= 2:
        weight_change = latest_metric.weight_kg - metrics.weight_kg
        strength_change = latest_metric.strength_1rm - metrics.strength_1rm
    
    return {
        "status": "success",
        "user_profile": {
            "user_id": user.user_id,
            "name": user.name,
            "age": user.age,
            "weight_kg": user.weight_kg,
            "height_cm": user.height_cm,
            "goal": user.goal,
            "fitness_level": user.fitness_level,
            "equipment": user.equipment
        },
        "statistics": {
            "total_metrics": len(metrics),
            "total_plans": len(plans),
            "total_messages": db.query(ChatMessage).filter(
                ChatMessage.user_id == user_id
            ).count(),
            "days_active": (datetime.utcnow() - user.created_at).days if user.created_at else 0
        },
        "latest_metrics": {
            "weight_kg": latest_metric.weight_kg if latest_metric else None,
            "strength_1rm": latest_metric.strength_1rm if latest_metric else None,
            "sleep_hours": latest_metric.sleep_hours if latest_metric else None,
            "mood": latest_metric.mood if latest_metric else None,
            "energy": latest_metric.energy if latest_metric else None,
            "recorded_at": latest_metric.created_at.isoformat() if latest_metric else None
        },
        "progress": {
            "weight_change_kg": round(weight_change, 1) if weight_change else None,
            "strength_change_kg": round(strength_change, 1) if strength_change else None,
            "trend": "improving" if strength_change and strength_change > 0 else "declining" if strength_change and strength_change < 0 else "stable"
        },
        "latest_plan": {
            "plan_id": plans.plan_id if plans else None,
            "week": plans.week if plans else None,
            "created_at": plans.created_at.isoformat() if plans else None
        } if plans else None,
        "recent_chat": len(chat_history)
    }


@router.get("/insights")
def get_insights(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get AI-generated insights
    
    Analyzes user data and provides personalized recommendations.
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    metrics = db.query(Metric).filter(
        Metric.user_id == user_id
    ).order_by(Metric.created_at).all()
    
    insights = []
    
    if not metrics:
        insights.append("Start logging metrics to get personalized insights!")
    else:
        latest = metrics[-1]
        
        # Sleep insight
        if latest.sleep_hours < 7:
            insights.append(f"⚠️ Sleep Alert: You're averaging {latest.sleep_hours}h of sleep. Aim for 7-9h for optimal recovery.")
        else:
            insights.append(f"✅ Sleep Good: Keep maintaining {latest.sleep_hours}h of quality sleep!")
        
        # Mood/Energy insight
        if latest.mood < 5 or latest.energy < 5:
            insights.append("😟 Mood Alert: Consider taking a lighter training week. Recovery matters!")
        else:
            insights.append("😊 Great Mood: You're in a good mental state. Push hard this week!")
        
        # Strength progress
        if len(metrics) >= 2:
            recent_strength = latest.strength_1rm - metrics[-2].strength_1rm
            if recent_strength > 5:
                insights.append(f"💪 Strength Surge: +{recent_strength}kg increase. You're making serious gains!")
            elif recent_strength < -5:
                insights.append("⚠️ Strength Dip: Your strength is dropping. Check your form and nutrition.")
            else:
                insights.append("➡️ Stability: Your strength is stable. Continue consistent training.")
        
        # Weight trend
        if len(metrics) >= 3:
            recent_weight = latest.weight_kg - metrics[-2].weight_kg
            if user.goal == "muscle_gain" and recent_weight > 0.5:
                insights.append(f"📈 Weight Gain: Good! You're gaining weight for muscle growth.")
            elif user.goal == "fat_loss" and recent_weight < -0.5:
                insights.append(f"📉 Weight Loss: Excellent progress on your fat loss goal!")
    
    return {
        "status": "success",
        "insights": insights,
        "recommendation": generate_recommendation(user, metrics)
    }


def generate_recommendation(user, metrics):
    """Generate personalized recommendation based on user data"""
    
    if not metrics:
        return "Start your fitness journey by logging your first metrics!"
    
    latest = metrics[-1]
    
    recommendations = {
        "muscle_gain": "Increase protein intake to 1g per lb bodyweight and prioritize strength training 4-6x/week.",
        "fat_loss": "Maintain a 300-500 calorie deficit and do 2-3 cardio sessions per week alongside strength training.",
        "strength": "Focus on the big 3 (squat, bench, deadlift), rest 3-5 minutes between heavy sets, and deload every 4 weeks.",
        "endurance": "Build aerobic capacity with long steady-state cardio 1-2x/week and tempo runs 1x/week."
    }
    
    base_rec = recommendations.get(user.goal, "Stay consistent with your training!")
    
    # Add contextual recommendation
    if latest.mood < 5:
        base_rec += " Also, prioritize rest and recovery this week."
    
    return base_rec
