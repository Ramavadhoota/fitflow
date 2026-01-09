from typing import Dict, List, Any


class DietAgent:
    """
    Generates personalized nutrition plans.
    
    Features:
    - TDEE calculation
    - Macro optimization (protein, carbs, fat)
    - Meal planning
    - Caloric surplus/deficit adjustment
    - Nutrient timing
    """
    
    def generate_nutrition_plan(
        self,
        user_profile: Dict[str, Any],
        week: int,
        metrics_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate weekly nutrition plan.
        
        Args:
            user_profile: User data (age, weight, height, goal, fitness_level)
            week: Week number (1-52)
            metrics_history: Historical metrics
        
        Returns:
            Complete nutrition plan with macros and meals
        """
        
        # Calculate TDEE (Total Daily Energy Expenditure)
        tdee = self._calculate_tdee(user_profile)
        
        # Get goal and adjust calories
        goal = user_profile.get("goal", "muscle_gain")
        daily_calories = self._adjust_calories_for_goal(tdee, goal)
        
        # Calculate macronutrients
        macros = self._calculate_macros(daily_calories, goal)
        
        # Generate meal plan
        meal_plan = self._generate_meal_plan(
            daily_calories, macros, user_profile
        )
        
        # Calculate nutrient timing
        timing = self._calculate_nutrient_timing(goal, user_profile)
        
        # Adjust based on progress
        adjustment = self._calculate_adjustment(week, metrics_history, goal)
        
        return {
            "week": week,
            "tdee": int(tdee),
            "daily_calories": int(daily_calories),
            "adjustment": adjustment,
            "macronutrients": {
                "protein_g": int(macros["protein"]),
                "carbs_g": int(macros["carbs"]),
                "fat_g": int(macros["fat"]),
                "protein_ratio": round(macros["protein_ratio"], 2),
                "carbs_ratio": round(macros["carbs_ratio"], 2),
                "fat_ratio": round(macros["fat_ratio"], 2)
            },
            "meals": meal_plan,
            "nutrient_timing": timing,
            "hydration_liters": self._calculate_hydration(user_profile),
            "supplementation": self._recommend_supplements(goal, user_profile)
        }
    
    def _calculate_tdee(self, user_profile: Dict[str, Any]) -> float:
        """
        Calculate Total Daily Energy Expenditure using Mifflin-St Jeor formula.
        
        Formula:
        Male: (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
        Female: (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161
        
        Then multiply by activity factor
        """
        
        weight_kg = user_profile.get("weight_kg", 70)
        height_cm = user_profile.get("height_cm", 175)
        age = user_profile.get("age", 30)
        fitness_level = user_profile.get("fitness_level", "intermediate")
        
        # Assume male (adjust for better accuracy)
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        
        # Activity multiplier
        activity_map = {
            "beginner": 1.4,      # 4-6 days training
            "intermediate": 1.55,  # 6-8 days training
            "advanced": 1.7       # 8+ days training
        }
        
        activity_multiplier = activity_map.get(fitness_level, 1.55)
        tdee = bmr * activity_multiplier
        
        return tdee
    
    def _adjust_calories_for_goal(self, tdee: float, goal: str) -> float:
        """Adjust calories based on goal"""
        
        adjustment_map = {
            "muscle_gain": tdee * 1.10,      # +10% surplus
            "fat_loss": tdee * 0.85,          # -15% deficit
            "strength": tdee * 1.05,          # +5% slight surplus
            "endurance": tdee * 0.95          # -5% slight deficit
        }
        
        return adjustment_map.get(goal, tdee)
    
    def _calculate_macros(self, daily_calories: float, goal: str) -> Dict[str, float]:
        """Calculate macronutrient targets"""
        
        macro_ratios = {
            "muscle_gain": {
                "protein_ratio": 0.30,
                "carbs_ratio": 0.50,
                "fat_ratio": 0.20
            },
            "fat_loss": {
                "protein_ratio": 0.35,
                "carbs_ratio": 0.40,
                "fat_ratio": 0.25
            },
            "strength": {
                "protein_ratio": 0.32,
                "carbs_ratio": 0.48,
                "fat_ratio": 0.20
            },
            "endurance": {
                "protein_ratio": 0.25,
                "carbs_ratio": 0.60,
                "fat_ratio": 0.15
            }
        }
        
        ratios = macro_ratios.get(goal, macro_ratios["muscle_gain"])
        
        protein = (daily_calories * ratios["protein_ratio"]) / 4
        carbs = (daily_calories * ratios["carbs_ratio"]) / 4
        fat = (daily_calories * ratios["fat_ratio"]) / 9
        
        return {
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "protein_ratio": ratios["protein_ratio"],
            "carbs_ratio": ratios["carbs_ratio"],
            "fat_ratio": ratios["fat_ratio"]
        }
    
    def _generate_meal_plan(
        self,
        daily_calories: float,
        macros: Dict,
        user_profile: Dict
    ) -> List[Dict[str, Any]]:
        """Generate daily meal plan"""
        
        meals_per_day = 4 if daily_calories > 2500 else 3
        calories_per_meal = daily_calories / meals_per_day
        
        meals = []
        meal_names = ["Breakfast", "Mid-Morning", "Lunch", "Dinner"]
        
        for i in range(meals_per_day):
            meals.append({
                "name": meal_names[i],
                "calories": int(calories_per_meal),
                "protein_g": int(macros["protein"] / meals_per_day),
                "carbs_g": int(macros["carbs"] / meals_per_day),
                "fat_g": int(macros["fat"] / meals_per_day),
                "examples": self._get_meal_examples(i, user_profile.get("goal"))
            })
        
        return meals
    
    def _get_meal_examples(self, meal_index: int, goal: str) -> List[str]:
        """Get meal examples based on timing"""
        
        examples_map = {
            0: ["Oatmeal with berries and almonds", "Eggs with toast", "Pancakes with protein"],
            1: ["Protein shake with banana", "Greek yogurt with granola", "Apple with peanut butter"],
            2: ["Chicken with rice and broccoli", "Salmon with sweet potato", "Lean beef with pasta"],
            3: ["Turkey and vegetables", "Fish with brown rice", "Lean meat with vegetables"]
        }
        
        return examples_map.get(meal_index, [])
    
    def _calculate_nutrient_timing(self, goal: str, user_profile: Dict) -> Dict:
        """Calculate nutrient timing around training"""
        
        return {
            "pre_workout": {
                "timing": "30-60 minutes before",
                "focus": "Carbs + Moderate Protein",
                "example": "Rice cakes with peanut butter"
            },
            "post_workout": {
                "timing": "30-60 minutes after",
                "focus": "Protein + Fast Carbs",
                "example": "Protein shake with dextrose"
            },
            "daily_distribution": "Spread protein evenly across meals (20-30g per meal)"
        }
    
    def _calculate_hydration(self, user_profile: Dict) -> float:
        """Calculate daily hydration target"""
        
        weight_kg = user_profile.get("weight_kg", 70)
        base_liters = weight_kg / 30  # Rough estimate
        training_boost = 0.5  # Extra for training days
        
        return round(base_liters + training_boost, 1)
    
    def _recommend_supplements(self, goal: str, user_profile: Dict) -> List[str]:
        """Recommend supplements based on goal"""
        
        base_supplements = ["Whey Protein", "Multivitamin", "Omega-3"]
        
        goal_supplements = {
            "muscle_gain": ["Creatine Monohydrate", "Dextrose PWO"],
            "fat_loss": ["Caffeine", "Green Tea Extract"],
            "strength": ["Creatine", "Beta-Alanine"],
            "endurance": ["Electrolytes", "BCAAs"]
        }
        
        return base_supplements + goal_supplements.get(goal, [])
    
    def _calculate_adjustment(
        self,
        week: int,
        metrics_history: List[Dict],
        goal: str
    ) -> str:
        """Calculate dietary adjustment needed"""
        
        if not metrics_history or len(metrics_history) < 2:
            return "Monitor progress for 1-2 weeks before adjusting"
        
        latest = metrics_history[-1]
        previous = metrics_history[-2]
        weight_change = latest.get("weight_kg", 0) - previous.get("weight_kg", 0)
        
        if goal == "muscle_gain":
            if weight_change < 0.2:
                return "Add 100-200 calories to surplus"
            else:
                return "Continue current intake"
        elif goal == "fat_loss":
            if weight_change > -0.2:
                return "Reduce 100 calories from deficit"
            else:
                return "Continue current deficit"
        
        return "Continue current nutrition plan"
