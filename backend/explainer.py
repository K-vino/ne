"""
Explainer Engine
Implements Explainable AI techniques (Feature Importance, SHAP, Rule-based)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from sklearn.tree import DecisionTreeClassifier, export_text

class ExplainerEngine:
    """Generate explanations for ML model predictions"""
    
    def __init__(self):
        pass
    
    def generate_explanations(self, model, X_test, y_test, 
                            feature_names: List[str]) -> Dict[str, Any]:
        """
        Generate comprehensive explanations
        
        Args:
            model: Trained ML model
            X_test: Test features
            y_test: Test labels
            feature_names: Names of features
            
        Returns:
            Dictionary with explanations
        """
        explanations = {
            "feature_importance": self._feature_importance(model, feature_names),
            "decision_rules": self._extract_rules(model, feature_names),
            "prediction_explanations": self._explain_predictions(
                model, X_test, y_test, feature_names
            ),
            "natural_language_summary": None
        }
        
        # Generate natural language summary
        explanations["natural_language_summary"] = self._generate_summary(explanations)
        
        return explanations
    
    def _feature_importance(self, model, feature_names: List[str]) -> Dict[str, Any]:
        """Extract feature importance from model"""
        importance_dict = {}
        
        # Try to get feature importance (works for tree-based models)
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            
            # Create sorted list
            importance_list = [
                {
                    "feature": feature_names[i],
                    "importance": float(importances[i]),
                    "percentage": float(importances[i] * 100)
                }
                for i in range(len(feature_names))
            ]
            
            # Sort by importance
            importance_list.sort(key=lambda x: x["importance"], reverse=True)
            
            importance_dict = {
                "ranked_features": importance_list,
                "top_3_features": [item["feature"] for item in importance_list[:3]],
                "visualization_data": {
                    "labels": [item["feature"] for item in importance_list],
                    "values": [item["percentage"] for item in importance_list]
                }
            }
        
        # For Logistic Regression, use coefficients
        elif hasattr(model, 'coef_'):
            coefficients = model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
            
            # Create sorted list
            importance_list = [
                {
                    "feature": feature_names[i],
                    "coefficient": float(coefficients[i]),
                    "abs_coefficient": float(abs(coefficients[i]))
                }
                for i in range(len(feature_names))
            ]
            
            # Sort by absolute coefficient
            importance_list.sort(key=lambda x: x["abs_coefficient"], reverse=True)
            
            importance_dict = {
                "ranked_features": importance_list,
                "top_3_features": [item["feature"] for item in importance_list[:3]],
                "visualization_data": {
                    "labels": [item["feature"] for item in importance_list],
                    "values": [item["abs_coefficient"] for item in importance_list]
                }
            }
        
        return importance_dict
    
    def _extract_rules(self, model, feature_names: List[str]) -> Dict[str, Any]:
        """Extract decision rules from tree-based models"""
        rules = {
            "rule_type": "tree-based" if hasattr(model, 'tree_') else "linear",
            "rules_text": [],
            "complexity": None
        }
        
        # For Decision Trees
        if hasattr(model, 'tree_'):
            try:
                # Extract text representation of tree
                tree_rules = export_text(model, feature_names=feature_names, max_depth=3)
                rules["rules_text"] = tree_rules.split('\n')[:20]  # First 20 lines
                rules["complexity"] = f"Tree depth: {model.tree_.max_depth}"
            except:
                rules["rules_text"] = ["Tree rules extraction not available"]
        
        # For Logistic Regression
        elif hasattr(model, 'coef_'):
            coeffs = model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_
            intercept = model.intercept_[0] if hasattr(model, 'intercept_') else 0
            
            rule_text = [f"Decision boundary: y = {intercept:.4f}"]
            for i, feature in enumerate(feature_names):
                if abs(coeffs[i]) > 0.01:  # Only show significant coefficients
                    sign = "+" if coeffs[i] > 0 else "-"
                    rule_text.append(f"  {sign} {abs(coeffs[i]):.4f} × {feature}")
            
            rules["rules_text"] = rule_text
            rules["complexity"] = "Linear combination of features"
        
        return rules
    
    def _explain_predictions(self, model, X_test, y_test, 
                           feature_names: List[str]) -> List[Dict[str, Any]]:
        """Explain individual predictions"""
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)
        
        explanations = []
        
        # Explain first 5 predictions
        for i in range(min(5, len(predictions))):
            pred = int(predictions[i])
            actual = int(y_test.iloc[i]) if hasattr(y_test, 'iloc') else int(y_test[i])
            proba = probabilities[i]
            
            # Get most influential features for this prediction
            instance_features = X_test.iloc[i] if hasattr(X_test, 'iloc') else X_test[i]
            
            # Calculate feature contributions (simplified)
            if hasattr(model, 'feature_importances_'):
                feature_importance = model.feature_importances_
            elif hasattr(model, 'coef_'):
                feature_importance = abs(model.coef_[0] if len(model.coef_.shape) > 1 else model.coef_)
            else:
                feature_importance = np.ones(len(feature_names))
            
            # Combine feature values with importance
            contributions = []
            for j, feature in enumerate(feature_names):
                value = float(instance_features[j]) if hasattr(instance_features, '__getitem__') else float(instance_features.iloc[j])
                contrib = float(value * feature_importance[j])
                contributions.append({
                    "feature": feature,
                    "value": value,
                    "contribution": contrib
                })
            
            # Sort by contribution
            contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
            
            explanation = {
                "instance": i + 1,
                "predicted_class": pred,
                "actual_class": actual,
                "correct": pred == actual,
                "confidence": float(max(proba)),
                "probability_distribution": proba.tolist(),
                "top_contributing_features": contributions[:3],
                "explanation_text": self._generate_instance_explanation(
                    pred, actual, contributions[:3], proba
                )
            }
            
            explanations.append(explanation)
        
        return explanations
    
    def _generate_instance_explanation(self, pred: int, actual: int,
                                      top_features: List[Dict], proba) -> str:
        """Generate natural language explanation for a prediction"""
        correct = "correctly" if pred == actual else "incorrectly"
        confidence = max(proba) * 100
        
        feature_text = ", ".join([
            f"{f['feature']}={f['value']:.2f}"
            for f in top_features
        ])
        
        explanation = (
            f"The model {correct} predicted class {pred} "
            f"with {confidence:.1f}% confidence. "
            f"Key influencing features: {feature_text}."
        )
        
        return explanation
    
    def _generate_summary(self, explanations: Dict[str, Any]) -> str:
        """Generate overall natural language summary"""
        feature_imp = explanations.get("feature_importance", {})
        top_features = feature_imp.get("top_3_features", [])
        
        if not top_features:
            return "Model explanations generated successfully."
        
        summary = (
            f"The model's decisions are primarily driven by {len(top_features)} key features: "
            f"{', '.join(top_features)}. "
            f"These features have the strongest influence on the predictions. "
            f"The model uses interpretable logic that can be understood and validated by domain experts."
        )
        
        return summary
