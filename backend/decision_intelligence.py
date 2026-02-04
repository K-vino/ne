"""
Decision Intelligence Module
Converts ML insights into actionable decision recommendations
"""

from typing import Dict, Any, List
import numpy as np

class DecisionIntelligence:
    """Generate decision recommendations with alternatives"""
    
    def __init__(self):
        pass
    
    def generate_recommendations(self, model_results: Dict[str, Any],
                                explanations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate decision recommendations based on model results and explanations
        
        Args:
            model_results: Results from ML model
            explanations: Explanations from XAI engine
            
        Returns:
            Dictionary with recommendations
        """
        # Get best model info
        best_model = model_results["best_model"]
        best_metrics = model_results["models"][best_model]["metrics"]
        
        # Get feature importance
        feature_importance = explanations.get("feature_importance", {})
        top_features = feature_importance.get("top_3_features", [])
        
        # Generate primary recommendation
        primary = self._generate_primary_recommendation(
            best_model, best_metrics, top_features
        )
        
        # Generate alternatives
        alternatives = self._generate_alternatives(model_results, explanations)
        
        # Calculate overall confidence
        overall_confidence = self._calculate_overall_confidence(best_metrics)
        
        recommendations = {
            "primary_recommendation": primary,
            "alternative_options": alternatives,
            "overall_confidence": overall_confidence,
            "decision_factors": self._extract_decision_factors(explanations),
            "risks_and_limitations": self._identify_risks(best_metrics),
            "human_considerations": self._generate_human_considerations()
        }
        
        return recommendations
    
    def _generate_primary_recommendation(self, model_name: str, 
                                        metrics: Dict[str, float],
                                        top_features: List[str]) -> Dict[str, Any]:
        """Generate primary recommendation"""
        accuracy = metrics["test_accuracy"]
        
        # Determine recommendation strength
        if accuracy >= 0.85:
            strength = "Strong"
            action = "Recommend proceeding with high confidence"
        elif accuracy >= 0.75:
            strength = "Moderate"
            action = "Recommend proceeding with caution"
        else:
            strength = "Weak"
            action = "Recommend further analysis before proceeding"
        
        recommendation = {
            "title": f"{strength} Recommendation Based on {model_name}",
            "action": action,
            "confidence_score": float(accuracy * 100),
            "confidence_level": self._map_confidence_level(accuracy),
            "key_factors": top_features,
            "reasoning": (
                f"Based on {model_name} analysis with {accuracy:.1%} accuracy, "
                f"the key factors influencing this decision are: {', '.join(top_features)}. "
                f"The model demonstrates {self._map_confidence_level(accuracy).lower()} confidence "
                "in its predictions."
            ),
            "recommended_action": self._suggest_action(accuracy),
            "priority": "High" if accuracy >= 0.8 else "Medium"
        }
        
        return recommendation
    
    def _generate_alternatives(self, model_results: Dict[str, Any],
                              explanations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alternative decision options"""
        alternatives = []
        
        # Alternative 1: Conservative approach
        alternatives.append({
            "option": "Conservative Approach",
            "description": "Proceed with additional validation and human oversight",
            "confidence": 85.0,
            "rationale": (
                "While the model provides insights, incorporating human expertise "
                "and domain knowledge will strengthen the decision-making process."
            ),
            "when_to_use": "When stakes are high or model confidence is moderate"
        })
        
        # Alternative 2: Data-driven approach
        best_score = model_results["best_score"]
        alternatives.append({
            "option": "Pure Data-Driven Approach",
            "description": "Rely primarily on model predictions",
            "confidence": float(best_score * 100),
            "rationale": (
                "The model has been validated and shows good performance. "
                "Following its recommendations closely can lead to efficient decisions."
            ),
            "when_to_use": "When model confidence is high and data quality is good"
        })
        
        # Alternative 3: Hybrid approach
        alternatives.append({
            "option": "Hybrid Approach",
            "description": "Combine model insights with expert judgment",
            "confidence": 90.0,
            "rationale": (
                "Leveraging both algorithmic insights and human intuition "
                "provides the most balanced and robust decision-making framework."
            ),
            "when_to_use": "Recommended for most scenarios (best practice)"
        })
        
        return alternatives
    
    def _calculate_overall_confidence(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Calculate overall confidence in recommendations"""
        accuracy = metrics["test_accuracy"]
        precision = metrics["precision"]
        recall = metrics["recall"]
        
        # Weighted average
        overall_score = (accuracy * 0.4 + precision * 0.3 + recall * 0.3) * 100
        
        return {
            "score": float(overall_score),
            "level": self._map_confidence_level(overall_score / 100),
            "components": {
                "accuracy": float(accuracy * 100),
                "precision": float(precision * 100),
                "recall": float(recall * 100)
            }
        }
    
    def _extract_decision_factors(self, explanations: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract key decision factors"""
        factors = []
        
        feature_importance = explanations.get("feature_importance", {})
        ranked_features = feature_importance.get("ranked_features", [])
        
        for i, feature_info in enumerate(ranked_features[:5]):  # Top 5
            factors.append({
                "rank": i + 1,
                "factor": feature_info.get("feature", "Unknown"),
                "importance": f"{feature_info.get('percentage', 0):.1f}%" if 'percentage' in feature_info else f"{feature_info.get('abs_coefficient', 0):.2f}",
                "impact": "High" if i < 2 else "Medium" if i < 4 else "Low"
            })
        
        return factors
    
    def _identify_risks(self, metrics: Dict[str, float]) -> List[str]:
        """Identify potential risks and limitations"""
        risks = []
        
        accuracy = metrics["test_accuracy"]
        train_acc = metrics["train_accuracy"]
        
        # Check for overfitting
        if train_acc - accuracy > 0.15:
            risks.append(
                "⚠️ Model shows signs of overfitting - predictions may not generalize well to new data"
            )
        
        # Check for low accuracy
        if accuracy < 0.75:
            risks.append(
                "⚠️ Model accuracy is below 75% - recommendations should be used with caution"
            )
        
        # General limitations
        risks.append(
            "ℹ️ Model is based on historical data - may not account for unprecedented scenarios"
        )
        risks.append(
            "ℹ️ Recommendations are probabilistic - human judgment is still essential"
        )
        
        return risks
    
    def _generate_human_considerations(self) -> List[str]:
        """Generate human-in-the-loop considerations"""
        return [
            "🧠 Review the top contributing features to ensure they align with domain knowledge",
            "🔍 Validate predictions against known cases or expert intuition",
            "⚖️ Consider ethical implications and fairness of the recommendation",
            "📊 Assess whether data quality and sample size are sufficient for this decision",
            "🎯 Define clear success criteria for evaluating the decision outcome"
        ]
    
    def _map_confidence_level(self, score: float) -> str:
        """Map confidence score to level"""
        if score >= 0.9:
            return "Very High"
        elif score >= 0.8:
            return "High"
        elif score >= 0.7:
            return "Moderate"
        elif score >= 0.6:
            return "Low"
        else:
            return "Very Low"
    
    def _suggest_action(self, accuracy: float) -> str:
        """Suggest specific action based on accuracy"""
        if accuracy >= 0.85:
            return "Implement recommendation with standard monitoring"
        elif accuracy >= 0.75:
            return "Implement with enhanced monitoring and review points"
        elif accuracy >= 0.65:
            return "Pilot test recommendation before full implementation"
        else:
            return "Gather more data or seek additional validation"
    
    def process_validation(self, feedback: Dict[str, Any],
                          recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Process human validation feedback"""
        decision = feedback["decision"]
        comments = feedback.get("comments", "")
        
        validation_result = {
            "decision_made": decision,
            "timestamp": None,  # Would use datetime in production
            "user_comments": comments,
            "original_recommendation": recommendations["primary_recommendation"]["title"],
            "confidence_alignment": None
        }
        
        # Assess alignment
        if decision == "accept":
            validation_result["confidence_alignment"] = "User agrees with recommendation"
            validation_result["outcome"] = "Recommendation accepted - proceeding as suggested"
        elif decision == "modify":
            validation_result["confidence_alignment"] = "User partially agrees with modifications"
            validation_result["outcome"] = "Recommendation modified based on user expertise"
            validation_result["modified_to"] = feedback.get("modified_recommendation", "")
        else:  # reject
            validation_result["confidence_alignment"] = "User disagrees with recommendation"
            validation_result["outcome"] = "Recommendation rejected - alternative approach needed"
        
        return validation_result
    
    def calculate_quality_metrics(self, validation: Dict[str, Any],
                                 model_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate decision quality metrics"""
        decision = validation["decision_made"]
        
        # Calculate clarity score (based on model performance)
        best_metrics = model_results["models"][model_results["best_model"]]["metrics"]
        clarity_score = best_metrics["test_accuracy"] * 100
        
        # Calculate confidence (simulated based on decision)
        if decision == "accept":
            user_confidence = 90
        elif decision == "modify":
            user_confidence = 70
        else:
            user_confidence = 40
        
        # Calculate trust (combination of metrics)
        trust_score = (clarity_score + user_confidence) / 2
        
        metrics = {
            "clarity": {
                "score": float(clarity_score),
                "description": "How clear and understandable the decision path is",
                "assessment": "High" if clarity_score >= 80 else "Moderate" if clarity_score >= 60 else "Low"
            },
            "confidence": {
                "score": float(user_confidence),
                "description": "User's confidence in the decision",
                "assessment": "High" if user_confidence >= 80 else "Moderate" if user_confidence >= 60 else "Low"
            },
            "trust": {
                "score": float(trust_score),
                "description": "Overall trust in the decision intelligence system",
                "assessment": "High" if trust_score >= 80 else "Moderate" if trust_score >= 60 else "Low"
            },
            "decision_summary": {
                "user_action": decision,
                "recommendation_followed": decision == "accept",
                "system_model": model_results["best_model"],
                "model_accuracy": float(best_metrics["test_accuracy"] * 100)
            }
        }
        
        return metrics
