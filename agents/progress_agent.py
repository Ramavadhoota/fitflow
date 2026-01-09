from typing import Dict, List, Any
from datetime import datetime, timedelta


class ProgressAgent:
    """
    Analyzes progress and predicts future results.
    
    Features:
    - Trend analysis (improving, stable, declining)
    - 4-week predictions
    - Recovery assessment
    - Anomaly detection
    """
    
    def analyze_progress(
        self,
        user_profile: Dict[str, Any],
        metrics_history: List[Dict[str, Any]],
        week: int
    ) -> Dict[str, Any]:
        """
        Analyze user progress and predict future results.
        
        Args:
            user_profile: User profile data
            metrics_history: Historical metrics
            week: Current week number
        
        Returns:
            Progress analysis with predictions
        """
        
        if not metrics_history or len(metrics_history) < 2:
            return self._insufficient_data_response(user_profile, week)
        
        # Calculate trends
        latest = metrics_history[-1]
        trend_data = self._calculate_trends(metrics_history)
        
        # Predict 4-week outlook
        predictions = self._predict_4weeks(
            metrics_history, user_profile.get("goal")
        )
        
        # Assess recovery
        recovery_score = self._assess_recovery(latest)
        
        # Detect anomalies
        anomalies = self._detect_anomalies(metrics_history)
        
        return {
            "week": week,
            "current_metrics": {
                "weight_kg": latest.get("weight_kg"),
                "strength_1rm": latest.get("strength_1rm"),
                "sleep_hours": latest.get("sleep_hours"),
                "mood": latest.get("mood"),
                "energy": latest.get("energy")
            },
            "trends": trend_data,
            "predictions_4week": predictions,
            "recovery_score": recovery_score,
            "anomalies": anomalies,
            "trend": self._get_overall_trend(trend_data)
        }
    
    def _insufficient_data_response(self, user_profile: Dict, week: int) -> Dict:
        """Return response when insufficient data"""
        
        return {
            "week": week,
            "status": "insufficient_data",
            "message": "Need 2+ weeks of data for analysis",
            "trend": "unknown",
            "recovery_score": 50
        }
    
    def _calculate_trends(self, metrics_history: List[Dict]) -> Dict[str, Dict]:
        """Calculate trends for all metrics"""
        
        if len(metrics_history) < 2:
            return {}
        
        latest = metrics_history[-1]
        previous = metrics_history[-2]
        
        return {
            "weight": {
                "current": latest.get("weight_kg"),
                "change_kg": round(latest.get("weight_kg", 0) - previous.get("weight_kg", 0), 1),
                "direction": "up" if latest.get("weight_kg", 0) > previous.get("weight_kg", 0) else "down"
            },
            "strength": {
                "current": latest.get("strength_1rm"),
                "change_kg": round(latest.get("strength_1rm", 0) - previous.get("strength_1rm", 0), 1),
                "direction": "up" if latest.get("strength_1rm", 0) > previous.get("strength_1rm", 0) else "down"
            },
            "sleep": {
                "current": latest.get("sleep_hours"),
                "change_hours": round(latest.get("sleep_hours", 0) - previous.get("sleep_hours", 0), 1)
            },
            "mood": {
                "current": latest.get("mood"),
                "change": latest.get("mood", 0) - previous.get("mood", 0)
            }
        }
    
    def _predict_4weeks(
        self,
        metrics_history: List[Dict],
        goal: str
    ) -> Dict[str, float]:
        """Predict metrics 4 weeks ahead"""
        
        if len(metrics_history) < 2:
            return {}
        
        latest = metrics_history[-1]
        
        if len(metrics_history) >= 5:
            # Linear regression with more data points
            recent_metrics = metrics_history[-5:]
            strength_trend = (recent_metrics[-1].get("strength_1rm", 0) - 
                            recent_metrics.get("strength_1rm", 0)) / 4
            weight_trend = (recent_metrics[-1].get("weight_kg", 0) - 
                          recent_metrics.get("weight_kg", 0)) / 4
        else:
            # Simple linear prediction
            strength_trend = latest.get("strength_1rm", 0) - metrics_history[-2].get("strength_1rm", 0)
            weight_trend = latest.get("weight_kg", 0) - metrics_history[-2].get("weight_kg", 0)
        
        predictions = {
            "strength_1rm_4w": round(latest.get("strength_1rm", 0) + (strength_trend * 4), 1),
            "weight_kg_4w": round(latest.get("weight_kg", 0) + (weight_trend * 4), 1),
            "strength_trend_per_week": round(strength_trend, 1),
            "weight_trend_per_week": round(weight_trend, 1)
        }
        
        # Add confidence based on data points
        confidence = min(0.85, 0.3 + (len(metrics_history) * 0.1))
        predictions["confidence"] = round(confidence, 2)
        
        return predictions
    
    def _assess_recovery(self, latest_metric: Dict) -> int:
        """
        Assess recovery quality (0-100).
        
        Based on: sleep, mood, energy
        """
        
        sleep_score = min(100, (latest_metric.get("sleep_hours", 0) / 9) * 100)
        mood_score = latest_metric.get("mood", 5) * 10
        energy_score = latest_metric.get("energy", 5) * 10
        
        recovery_score = (sleep_score * 0.4) + (mood_score * 0.3) + (energy_score * 0.3)
        
        return int(min(100, max(0, recovery_score)))
    
    def _detect_anomalies(self, metrics_history: List[Dict]) -> List[str]:
        """Detect anomalies in metrics"""
        
        anomalies = []
        latest = metrics_history[-1]
        
        # Check if mood or energy dipped
        if latest.get("mood", 5) < 4:
            anomalies.append("Low mood detected - consider deload week")
        
        if latest.get("energy", 5) < 4:
            anomalies.append("Low energy - check sleep and nutrition")
        
        # Check for weight fluctuations
        if len(metrics_history) >= 2:
            weight_change = abs(latest.get("weight_kg", 0) - metrics_history[-2].get("weight_kg", 0))
            if weight_change > 3:
                anomalies.append(f"Large weight change ({weight_change}kg) - may be water retention")
        
        # Check for strength drops
        if len(metrics_history) >= 2:
            strength_change = latest.get("strength_1rm", 0) - metrics_history[-2].get("strength_1rm", 0)
            if strength_change < -10:
                anomalies.append("Significant strength drop - check form and recovery")
        
        return anomalies
    
    def _get_overall_trend(self, trend_data: Dict) -> str:
        """Determine overall trend"""
        
        if not trend_data:
            return "unknown"
        
        strength_direction = trend_data.get("strength", {}).get("direction", "")
        
        if strength_direction == "up":
            return "increasing"
        elif strength_direction == "down":
            return "declining"
        else:
            return "stable"