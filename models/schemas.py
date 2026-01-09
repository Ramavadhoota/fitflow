from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# ==========================================
# USER SCHEMAS
# ==========================================

class UserRegister(BaseModel):
    """Schema for user registration"""
    user_id: str
    name: str
    age: int
    weight_kg: float
    height_cm: int
    fitness_level: str
    goal: str
    equipment: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alice",
                "name": "Alice Smith",
                "age": 28,
                "weight_kg": 65,
                "height_cm": 165,
                "fitness_level": "intermediate",
                "goal": "muscle_gain",
                "equipment": ["dumbbells", "barbell"]
            }
        }


class UserProfile(BaseModel):
    """Schema for user profile response"""
    user_id: str
    name: str
    age: int
    weight_kg: float
    height_cm: int
    fitness_level: str
    goal: str
    equipment: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==========================================
# METRIC SCHEMAS
# ==========================================

class MetricLog(BaseModel):
    """Schema for logging metrics"""
    user_id: str
    weight_kg: float
    strength_1rm: float
    sleep_hours: float
    mood: int
    energy: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alice",
                "weight_kg": 65.5,
                "strength_1rm": 185,
                "sleep_hours": 7.5,
                "mood": 8,
                "energy": 8
            }
        }


class MetricResponse(BaseModel):
    """Schema for metric response"""
    weight_kg: float
    strength_1rm: float
    sleep_hours: float
    mood: int
    energy: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==========================================
# PLAN SCHEMAS
# ==========================================

class PlanRequest(BaseModel):
    """Schema for requesting a plan"""
    user_id: str
    week: int = 1
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alice",
                "week": 1
            }
        }


class WorkoutPlan(BaseModel):
    """Schema for workout plan"""
    split_type: str
    frequency: int
    exercises: List[Dict[str, Any]]
    week: int
    progression: str


class NutritionPlan(BaseModel):
    """Schema for nutrition plan"""
    daily_calories: int
    protein_g: int
    carbs_g: int
    fat_g: int
    meals: int
    week: int


class CoachingPlan(BaseModel):
    """Schema for coaching plan"""
    strategy: str
    barriers: List[str]
    habit_stack: str
    touchpoints: List[str]
    week: int


class PlanResponse(BaseModel):
    """Schema for complete plan response"""
    status: str
    plan_id: str
    components: Dict[str, Any]
    summary: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "plan_id": "plan_1704516124.5678",
                "components": {
                    "workout": {
                        "split_type": "PPL",
                        "frequency": 6,
                        "exercises": 9
                    },
                    "nutrition": {
                        "daily_calories": 2833,
                        "protein_g": 212
                    },
                    "coaching": {
                        "strategy": "Daily check-ins"
                    }
                },
                "summary": "Week 1: PPL training, 2833kcal..."
            }
        }


# ==========================================
# CHAT SCHEMAS
# ==========================================

class ChatMessage(BaseModel):
    """Schema for chat message"""
    user_id: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "alice",
                "message": "How can I improve my gains?"
            }
        }


class ChatResponse(BaseModel):
    """Schema for chat response"""
    status: str
    response: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "response": "Based on your goal, here's my advice..."
            }
        }


# ==========================================
# RESPONSE SCHEMAS
# ==========================================

class SuccessResponse(BaseModel):
    """Generic success response"""
    status: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Generic error response"""
    status: str
    error: str
    detail: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "error": "User not found",
                "detail": "No user with ID 'alice' exists"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    environment: str
    version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "environment": "development",
                "version": "1.0.0"
            }
        }


# ==========================================
# PREDICTION SCHEMAS
# ==========================================

class PredictionResponse(BaseModel):
    """Schema for prediction response"""
    status: str
    predictions: Dict[str, Any]
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "predictions": {
                    "strength_4w": 215.0,
                    "confidence": 0.85
                }
            }
        }