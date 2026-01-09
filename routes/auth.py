from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.entities import User, get_db
from models.schemas import UserRegister, UserProfile, SuccessResponse

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}}
)


@router.post("/register", response_model=SuccessResponse)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    Creates a new user profile with fitness goals and preferences.
    
    Example request:
    ```json
    {
        "user_id": "alice",
        "name": "Alice Smith",
        "age": 28,
        "weight_kg": 65,
        "height_cm": 165,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["dumbbells", "barbell"]
    }
    ```
    
    Response:
    ```json
    {
        "status": "success",
        "message": "User 'alice' registered successfully"
    }
    ```
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.user_id == user_data.user_id
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=f"User with ID '{user_data.user_id}' already exists"
        )
    
    # Validate fitness level
    valid_levels = ["beginner", "intermediate", "advanced"]
    if user_data.fitness_level.lower() not in valid_levels:
        raise HTTPException(
            status_code=400,
            detail=f"Fitness level must be one of: {', '.join(valid_levels)}"
        )
    
    # Validate goal
    valid_goals = ["muscle_gain", "fat_loss", "strength", "endurance"]
    if user_data.goal.lower() not in valid_goals:
        raise HTTPException(
            status_code=400,
            detail=f"Goal must be one of: {', '.join(valid_goals)}"
        )
    
    # Validate age
    if user_data.age < 13 or user_data.age > 120:
        raise HTTPException(
            status_code=400,
            detail="Age must be between 13 and 120"
        )
    
    # Validate weight
    if user_data.weight_kg < 30 or user_data.weight_kg > 300:
        raise HTTPException(
            status_code=400,
            detail="Weight must be between 30 and 300 kg"
        )
    
    # Validate height
    if user_data.height_cm < 100 or user_data.height_cm > 250:
        raise HTTPException(
            status_code=400,
            detail="Height must be between 100 and 250 cm"
        )
    
    # Create new user
    db_user = User(
        user_id=user_data.user_id,
        name=user_data.name,
        age=user_data.age,
        weight_kg=user_data.weight_kg,
        height_cm=user_data.height_cm,
        fitness_level=user_data.fitness_level.lower(),
        goal=user_data.goal.lower(),
        equipment=user_data.equipment
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "status": "success",
        "message": f"User '{user_data.user_id}' registered successfully"
    }


@router.get("/profile", response_model=UserProfile)
def get_profile(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get user profile
    
    Retrieves complete user profile information.
    
    Query parameters:
    - user_id: The user ID to retrieve
    
    Example request:
    ```
    GET /api/v1/auth/profile?user_id=alice
    ```
    
    Response:
    ```json
    {
        "user_id": "alice",
        "name": "Alice Smith",
        "age": 28,
        "weight_kg": 65,
        "height_cm": 165,
        "fitness_level": "intermediate",
        "goal": "muscle_gain",
        "equipment": ["dumbbells", "barbell"],
        "created_at": "2026-01-06T12:25:00Z"
    }
    ```
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    return user


@router.put("/profile")
def update_profile(
    user_id: str,
    updates: dict,
    db: Session = Depends(get_db)
):
    """
    Update user profile
    
    Updates specific fields in user profile.
    Allows updating: weight_kg, fitness_level, goal, equipment
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    # Allowed fields to update
    allowed_fields = ["weight_kg", "fitness_level", "goal", "equipment"]
    
    for field, value in updates.items():
        if field not in allowed_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot update field '{field}'. Allowed: {allowed_fields}"
            )
        
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return {
        "status": "success",
        "message": f"User '{user_id}' profile updated",
        "user": user
    }


@router.delete("/profile")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete user account
    
    Deletes user and all associated data (metrics, plans, messages).
    WARNING: This cannot be undone!
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User '{user_id}' not found"
        )
    
    db.delete(user)
    db.commit()
    
    return {
        "status": "success",
        "message": f"User '{user_id}' deleted successfully"
    }