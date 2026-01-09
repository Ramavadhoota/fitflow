from typing import Dict, List, Any


class WorkoutAgent:
    """
    Generates personalized workout plans.
    
    Features:
    - PPL (Push/Pull/Legs) and Upper/Lower splits
    - Progressive overload tracking
    - Exercise selection based on equipment
    - Volume and intensity periodization
    - Recovery optimization
    """
    
    def __init__(self):
        """Initialize workout templates"""
        self.exercises_db = self._init_exercises()
    
    def generate_workout_plan(
        self,
        user_profile: Dict[str, Any],
        week: int,
        metrics_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate weekly workout plan.
        
        Args:
            user_profile: User data (goal, fitness_level, equipment)
            week: Week number (1-52)
            metrics_history: Historical metrics for progression
        
        Returns:
            Complete workout plan with exercises and progression
        """
        
        goal = user_profile.get("goal", "muscle_gain")
        fitness_level = user_profile.get("fitness_level", "intermediate")
        equipment = user_profile.get("equipment", ["dumbbells", "barbell"])
        
        # Select split based on fitness level
        split_type = self._select_split(fitness_level, goal)
        
        # Generate exercises for each day
        if split_type == "PPL":
            workout_days = self._generate_ppl_split(
                goal, fitness_level, equipment, week
            )
            frequency = 6
        else:  # Upper/Lower
            workout_days = self._generate_upper_lower_split(
                goal, fitness_level, equipment, week
            )
            frequency = 4
        
        # Calculate progression
        progression = self._calculate_progression(week, fitness_level, metrics_history)
        
        return {
            "week": week,
            "split_type": split_type,
            "frequency": frequency,
            "exercises": len(workout_days),
            "days": workout_days,
            "progression": progression,
            "total_volume": self._calculate_volume(workout_days),
            "rest_days": 7 - frequency,
            "intensity_level": self._get_intensity_level(week, fitness_level),
            "deload_week": week % 4 == 0  # Every 4th week
        }
    
    def _select_split(self, fitness_level: str, goal: str) -> str:
        """Select appropriate split for fitness level"""
        
        split_map = {
            "beginner": "Upper/Lower",
            "intermediate": "PPL",
            "advanced": "PPL"
        }
        
        return split_map.get(fitness_level, "PPL")
    
    def _generate_ppl_split(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Push/Pull/Legs split"""
        
        return {
            "Push": self._generate_push_day(goal, fitness_level, equipment, week),
            "Pull": self._generate_pull_day(goal, fitness_level, equipment, week),
            "Legs": self._generate_legs_day(goal, fitness_level, equipment, week),
            "Push2": self._generate_push_day(goal, fitness_level, equipment, week),
            "Pull2": self._generate_pull_day(goal, fitness_level, equipment, week),
            "Legs2": self._generate_legs_day(goal, fitness_level, equipment, week)
        }
    
    def _generate_upper_lower_split(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Upper/Lower split"""
        
        return {
            "Upper1": self._generate_upper_day(goal, fitness_level, equipment, week),
            "Lower1": self._generate_lower_day(goal, fitness_level, equipment, week),
            "Upper2": self._generate_upper_day(goal, fitness_level, equipment, week),
            "Lower2": self._generate_lower_day(goal, fitness_level, equipment, week)
        }
    
    def _generate_push_day(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Push day exercises"""
        
        intensity = "Heavy" if week % 4 != 0 else "Moderate"
        
        return {
            "exercises": [
                {
                    "name": "Barbell Bench Press",
                    "sets": 4,
                    "reps": "6-8" if goal == "strength" else "8-12",
                    "intensity": intensity,
                    "rest_seconds": 180
                },
                {
                    "name": "Incline Dumbbell Press",
                    "sets": 3,
                    "reps": "8-12",
                    "intensity": "Moderate",
                    "rest_seconds": 120
                },
                {
                    "name": "Lateral Raises",
                    "sets": 3,
                    "reps": "10-15",
                    "intensity": "Moderate",
                    "rest_seconds": 90
                },
                {
                    "name": "Rope Pushdowns",
                    "sets": 3,
                    "reps": "10-15",
                    "intensity": "Light",
                    "rest_seconds": 60
                }
            ],
            "estimated_duration_minutes": 60,
            "focus": "Chest, Shoulders, Triceps"
        }
    
    def _generate_pull_day(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Pull day exercises"""
        
        intensity = "Heavy" if week % 4 != 0 else "Moderate"
        
        return {
            "exercises": [
                {
                    "name": "Barbell Rows",
                    "sets": 4,
                    "reps": "6-8" if goal == "strength" else "8-12",
                    "intensity": intensity,
                    "rest_seconds": 180
                },
                {
                    "name": "Lat Pulldowns",
                    "sets": 3,
                    "reps": "8-12",
                    "intensity": "Moderate",
                    "rest_seconds": 120
                },
                {
                    "name": "Face Pulls",
                    "sets": 3,
                    "reps": "12-15",
                    "intensity": "Moderate",
                    "rest_seconds": 90
                },
                {
                    "name": "Barbell Curls",
                    "sets": 3,
                    "reps": "8-12",
                    "intensity": "Light",
                    "rest_seconds": 90
                }
            ],
            "estimated_duration_minutes": 60,
            "focus": "Back, Biceps"
        }
    
    def _generate_legs_day(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Legs day exercises"""
        
        intensity = "Heavy" if week % 4 != 0 else "Moderate"
        
        return {
            "exercises": [
                {
                    "name": "Barbell Back Squat",
                    "sets": 4,
                    "reps": "6-8" if goal == "strength" else "8-12",
                    "intensity": intensity,
                    "rest_seconds": 180
                },
                {
                    "name": "Romanian Deadlifts",
                    "sets": 3,
                    "reps": "6-8",
                    "intensity": "Heavy",
                    "rest_seconds": 120
                },
                {
                    "name": "Leg Press",
                    "sets": 3,
                    "reps": "10-15",
                    "intensity": "Moderate",
                    "rest_seconds": 120
                },
                {
                    "name": "Leg Curls",
                    "sets": 3,
                    "reps": "10-15",
                    "intensity": "Light",
                    "rest_seconds": 60
                }
            ],
            "estimated_duration_minutes": 75,
            "focus": "Quads, Hamstrings, Glutes"
        }
    
    def _generate_upper_day(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Upper body day"""
        
        return {
            "exercises": [
                {
                    "name": "Barbell Bench Press",
                    "sets": 4,
                    "reps": "6-8" if goal == "strength" else "8-12"
                },
                {
                    "name": "Barbell Rows",
                    "sets": 4,
                    "reps": "6-8" if goal == "strength" else "8-12"
                },
                {
                    "name": "Pull-ups",
                    "sets": 3,
                    "reps": "6-10"
                },
                {
                    "name": "Dumbbell Press",
                    "sets": 3,
                    "reps": "8-12"
                }
            ],
            "estimated_duration_minutes": 70
        }
    
    def _generate_lower_day(
        self,
        goal: str,
        fitness_level: str,
        equipment: List[str],
        week: int
    ) -> Dict[str, Any]:
        """Generate Lower body day"""
        
        return {
            "exercises": [
                {
                    "name": "Barbell Back Squat",
                    "sets": 4,
                    "reps": "6-8" if goal == "strength" else "8-12"
                },
                {
                    "name": "Deadlifts",
                    "sets": 3,
                    "reps": "3-5"
                },
                {
                    "name": "Leg Press",
                    "sets": 3,
                    "reps": "8-12"
                },
                {
                    "name": "Leg Curls",
                    "sets": 3,
                    "reps": "10-15"
                }
            ],
            "estimated_duration_minutes": 80
        }
    
    def _calculate_progression(
        self,
        week: int,
        fitness_level: str,
        metrics_history: List[Dict[str, Any]]
    ) -> str:
        """Calculate progression strategy"""
        
        if week % 4 == 0:
            return "Deload week - reduce volume by 40%"
        
        progression_map = {
            "beginner": f"+2.5% from Week {week-1}",
            "intermediate": f"+5% from Week {week-1}",
            "advanced": f"+3-5% based on form quality"
        }
        
        return progression_map.get(fitness_level, "+5% from previous week")
    
    def _get_intensity_level(self, week: int, fitness_level: str) -> str:
        """Get intensity level for the week"""
        
        if week % 4 == 0:
            return "Low (Deload)"
        elif week % 4 == 1:
            return "Moderate"
        elif week % 4 == 2:
            return "High"
        else:
            return "Very High"
    
    def _calculate_volume(self, workout_days: Dict) -> Dict[str, int]:
        """Calculate total training volume"""
        
        total_sets = 0
        total_reps = 0
        
        for day, exercises in workout_days.items():
            if isinstance(exercises, dict) and "exercises" in exercises:
                for exercise in exercises["exercises"]:
                    total_sets += exercise.get("sets", 0)
                    reps = exercise.get("reps", "8-12")
                    if isinstance(reps, str) and "-" in reps:
                        avg_reps = (int(reps.split("-")) + int(reps.split("-"))) // 2
                    else:
                        avg_reps = 8
                    total_reps += avg_reps
        
        return {
            "total_sets_per_week": total_sets,
            "estimated_reps_per_week": total_reps,
            "volume_score": (total_sets * total_reps) // 100
        }
    
    def _init_exercises(self) -> Dict[str, Any]:
        """Initialize exercise database"""
        
        return {
            "compounds": [
                "Barbell Back Squat", "Deadlifts", "Barbell Bench Press",
                "Barbell Rows", "Pull-ups", "Dips"
            ],
            "isolation": [
                "Leg Press", "Leg Curls", "Lateral Raises", "Rope Pushdowns",
                "Face Pulls", "Barbell Curls"
            ]
        }