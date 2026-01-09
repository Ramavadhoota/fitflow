from typing import Dict, List, Any


class CoachingAgent:
    """
    Generates behavioral coaching strategies.
    
    Features:
    - Motivation strategies
    - Habit stacking
    - Barrier identification
    - Adherence optimization
    - Personalized touchpoints
    """
    
    def generate_coaching_strategy(
        self,
        user_profile: Dict[str, Any],
        progress_analysis: Dict[str, Any],
        week: int,
        metrics_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate personalized coaching strategy.
        
        Args:
            user_profile: User profile
            progress_analysis: Progress trends and predictions
            week: Current week
            metrics_history: Historical metrics
        
        Returns:
            Coaching strategy with motivation and habits
        """
        
        goal = user_profile.get("goal", "muscle_gain")
        fitness_level = user_profile.get("fitness_level", "intermediate")
        
        # Identify barriers
        barriers = self._identify_barriers(
            user_profile, progress_analysis, metrics_history
        )
        
        # Generate motivation strategy
        motivation = self._generate_motivation(goal, fitness_level, week)
        
        # Create habit stack
        habit_stack = self._create_habit_stack(goal, fitness_level)
        
        # Identify touchpoints
        touchpoints = self._generate_touchpoints(goal, week)
        
        return {
            "week": week,
            "strategy": motivation,
            "barriers": barriers,
            "barrier_solutions": self._solve_barriers(barriers),
            "habit_stack": habit_stack,
            "daily_touchpoints": touchpoints,
            "weekly_check_in": self._generate_check_in(goal, week),
            "motivational_quote": self._get_motivational_quote(goal)
        }
    
    def _identify_barriers(
        self,
        user_profile: Dict,
        progress_analysis: Dict,
        metrics_history: List[Dict]
    ) -> List[str]:
        """Identify potential barriers to success"""
        
        barriers = []
        
        # Check recovery
        recovery_score = progress_analysis.get("recovery_score", 70)
        if recovery_score < 60:
            barriers.append("Poor recovery - sleep or stress management needed")
        
        # Check mood
        if metrics_history:
            latest = metrics_history[-1]
            if latest.get("mood", 5) < 5:
                barriers.append("Low motivation - consider variety in training")
        
        # Check anomalies
        anomalies = progress_analysis.get("anomalies", [])
        if anomalies:
            barriers.extend(anomalies[:2])
        
        return barriers if barriers else ["No major barriers detected"]
    
    def _solve_barriers(self, barriers: List[str]) -> Dict[str, str]:
        """Provide solutions for identified barriers"""
        
        solutions = {}
        
        for barrier in barriers:
            if "recovery" in barrier.lower():
                solutions[barrier] = "Increase sleep by 30 min, reduce stress, ensure 1-2 rest days/week"
            elif "motivation" in barrier.lower():
                solutions[barrier] = "Try new exercises, train with friends, vary workout split"
            elif "strength drop" in barrier.lower():
                solutions[barrier] = "Take a deload week, check exercise form, ensure adequate nutrition"
            elif "weight" in barrier.lower():
                solutions[barrier] = "Adjust caloric intake by 100-200 calories, increase water intake"
            else:
                solutions[barrier] = "Address this issue in your next training session"
        
        return solutions
    
    def _generate_motivation(self, goal: str, fitness_level: str, week: int) -> str:
        """Generate motivational strategy"""
        
        strategies = {
            "muscle_gain": "Focus on progressive overload - chase strength gains daily!",
            "fat_loss": "Remember your why - visualize your goal body daily",
            "strength": "Every PR is a win - document your progress religiously",
            "endurance": "Build consistency first - speed comes with time"
        }
        
        base_strategy = strategies.get(goal, "Stay consistent!")
        
        # Add week-specific motivation
        if week % 4 == 0:
            base_strategy += " This is deload week - focus on recovery and technique!"
        elif week % 4 == 1:
            base_strategy += " Fresh week incoming - reset your mindset!"
        
        return base_strategy
    
    def _create_habit_stack(self, goal: str, fitness_level: str) -> List[Dict[str, str]]:
        """Create habit stacking framework"""
        
        habit_stacks = {
            "beginner": [
                {
                    "trigger": "Morning alarm",
                    "habit": "Drink 500ml water",
                    "reward": "Coffee or breakfast"
                },
                {
                    "trigger": "Before bed",
                    "habit": "Log your metrics",
                    "reward": "Phone time"
                }
            ],
            "intermediate": [
                {
                    "trigger": "Pre-workout",
                    "habit": "Warm-up 5 min",
                    "reward": "First set is easier"
                },
                {
                    "trigger": "Post-workout",
                    "habit": "Protein shake",
                    "reward": "Recovery tracking"
                }
            ],
            "advanced": [
                {
                    "trigger": "Morning",
                    "habit": "Review week's plan",
                    "reward": "Mental preparation"
                },
                {
                    "trigger": "Training",
                    "habit": "Track all metrics",
                    "reward": "See progress data"
                }
            ]
        }
        
        return habit_stacks.get(fitness_level, habit_stacks["intermediate"])
    
    def _generate_touchpoints(self, goal: str, week: int) -> List[str]:
        """Generate daily touchpoints"""
        
        touchpoints = [
            "Morning: Check nutrition plan for today",
            "Pre-workout: 5 min mental prep",
            "Post-workout: Log your metrics immediately",
            "Evening: Reflect on adherence"
        ]
        
        if week % 2 == 0:
            touchpoints.append("Weekly check-in: Review progress against goals")
        
        return touchpoints
    
    def _generate_check_in(self, goal: str, week: int) -> Dict[str, Any]:
        """Generate weekly check-in questions"""
        
        return {
            "week": week,
            "questions": [
                "How consistent were you with your workout plan? (1-10)",
                "How consistent were you with your nutrition? (1-10)",
                "How was your recovery and sleep quality? (1-10)",
                "Did you achieve your main goal this week?"
            ],
            "reflection": "Celebrate wins, learn from misses, plan improvements"
        }
    
    def _get_motivational_quote(self, goal: str) -> str:
        """Get motivational quote"""
        
        quotes = {
            "muscle_gain": "The pump is temporary, but gains are forever.",
            "fat_loss": "Progress over perfection - every rep counts.",
            "strength": "Strength is earned through consistent effort.",
            "endurance": "Consistency beats intensity every time."
        }
        
        return quotes.get(goal, "Every workout is a win.")
