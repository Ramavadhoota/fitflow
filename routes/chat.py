from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.entities import User, ChatMessage, get_db
from models.schemas import ChatMessage as ChatSchema, ChatResponse, SuccessResponse

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}}
)


@router.post("/message", response_model=ChatResponse)
def send_message(
    chat_msg: ChatSchema,
    db: Session = Depends(get_db)
):
    """
    Chat with AI fitness coach
    
    Send messages to get personalized fitness advice based on user's goal
    and current progress.
    
    Uses behavioral coaching agent to provide:
    - Motivation strategies
    - Habit stacking suggestions
    - Barrier removal advice
    - Progress encouragement
    
    Example request:
    ```json
    {
        "user_id": "alice",
        "message": "How can I improve my gains?"
    }
    ```
    
    Response:
    ```json
    {
        "status": "success",
        "response": "Based on your muscle_gain goal, here's my advice: ..."
    }
    ```
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == chat_msg.user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{chat_msg.user_id}' not found"
        )
    
    # Generate response based on user's goal and message
    response = generate_coaching_response(
        user_id=chat_msg.user_id,
        goal=user.goal,
        fitness_level=user.fitness_level,
        message=chat_msg.message,
        db=db
    )
    
    # Save chat to database
    db_chat = ChatMessage(
        user_id=chat_msg.user_id,
        user_message=chat_msg.message,
        bot_response=response
    )
    
    db.add(db_chat)
    db.commit()
    
    return {
        "status": "success",
        "response": response
    }


@router.get("/history")
def get_chat_history(
    user_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get chat history
    
    Retrieves conversation history with AI coach.
    
    Query parameters:
    - user_id: The user ID
    - limit: Maximum messages to return (default: 20)
    
    Example request:
    ```
    GET /api/v1/chat/history?user_id=alice&limit=10
    ```
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    if not messages:
        raise HTTPException(
            status_code=404,
            detail=f"No chat messages found for user '{user_id}'"
        )
    
    return {
        "status": "success",
        "count": len(messages),
        "messages": [
            {
                "user_message": m.user_message,
                "bot_response": m.bot_response,
                "created_at": m.created_at.isoformat()
            }
            for m in reversed(messages)
        ]
    }


@router.delete("/history")
def clear_chat_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Clear chat history
    
    Deletes all chat messages for a user.
    WARNING: This cannot be undone!
    """
    # Verify user exists
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    # Delete all messages
    db.query(ChatMessage).filter(
        ChatMessage.user_id == user_id
    ).delete()
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Chat history cleared successfully"
    }


def generate_coaching_response(
    user_id: str,
    goal: str,
    fitness_level: str,
    message: str,
    db: Session
) -> str:
    """
    Generate AI coaching response
    
    Creates personalized response based on user's goal and question.
    """
    
    # Get user's latest metrics for context
    from models.entities import Metric
    latest_metric = db.query(Metric).filter(
        Metric.user_id == user_id
    ).order_by(Metric.created_at.desc()).first()
    
    goal_advice = {
        "muscle_gain": "Focus on progressive overload, high protein intake (1g per lb bodyweight), and adequate sleep. Consistency is key!",
        "fat_loss": "Create a caloric deficit of 300-500 calories, maintain high protein to preserve muscle, and track your macros closely.",
        "strength": "Prioritize compound movements (squat, bench, deadlift), progressive overload, and adequate rest between sets. Minimum 3-4 days training.",
        "endurance": "Build your aerobic base with steady-state cardio 3-4x/week, incorporate interval training 1-2x/week, and focus on recovery."
    }
    
    level_advice = {
        "beginner": "You're starting your fitness journey! Focus on learning proper form first, consistency over intensity, and building habits.",
        "intermediate": "You have a solid foundation! Challenge yourself with progressive overload, varied rep ranges, and advanced programming.",
        "advanced": "You're experienced! Fine-tune your approach with periodization, advanced techniques, and listen to your body's signals."
    }
    
    base_response = f"Based on your {goal} goal, {goal_advice.get(goal, 'stay consistent with training and nutrition.')} {level_advice.get(fitness_level, '')}"
    
    # Add metric context if available
    if latest_metric:
        if latest_metric.mood < 5:
            base_response += " I notice your mood might be low - make sure you're getting quality sleep and managing stress."
        if latest_metric.sleep_hours < 7:
            base_response += " Your sleep seems low - aim for 7-9 hours for optimal recovery and hormone balance."
    
    # Answer specific questions
    if "sleep" in message.lower():
        base_response += " Sleep is crucial! Aim for 7-9 hours, maintain a consistent schedule, and keep your room cool and dark."
    elif "motivation" in message.lower():
        base_response += " Stay motivated by tracking progress visually, celebrating small wins, and remembering why you started!"
    elif "plateau" in message.lower():
        base_response += " Plateaus are normal! Try varying your rep ranges, changing exercises, or increasing training frequency."
    elif "nutrition" in message.lower():
        base_response += " Nutrition is 70% of the battle. Track your macros, stay consistent, and adjust based on results."
    elif "recovery" in message.lower():
        base_response += " Recovery is when the gains happen! Prioritize sleep, manage stress, and consider deload weeks every 4-6 weeks."
    
    return base_response