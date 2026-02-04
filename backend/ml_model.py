"""
ML Model Engine
Implements interpretable ML models (Decision Tree, Logistic Regression)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from typing import Dict, Any, List

class MLModelEngine:
    """Train and evaluate interpretable ML models"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        
    def train_and_evaluate(self, df: pd.DataFrame, features: List[str], 
                          target: str) -> Dict[str, Any]:
        """
        Train multiple interpretable models and evaluate them
        
        Args:
            df: DataFrame with features and target
            features: List of feature column names
            target: Target column name
            
        Returns:
            Dictionary with model results
        """
        # Prepare data
        X = df[features].copy()
        y = df[target].copy()
        
        # Handle categorical target (convert to numeric if needed)
        if y.dtype == 'object':
            y = pd.Categorical(y).codes
        
        # Store feature names
        self.feature_names = features
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Initialize models (interpretable ones only)
        self.models = {
            "Decision Tree": DecisionTreeClassifier(
                max_depth=5,  # Limit depth for interpretability
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=42
            ),
            "Logistic Regression": LogisticRegression(
                max_iter=1000,
                random_state=42
            ),
            "Random Forest": RandomForestClassifier(
                n_estimators=50,
                max_depth=5,
                min_samples_split=10,
                random_state=42
            )
        }
        
        # Train and evaluate each model
        results = {
            "models": {},
            "best_model": None,
            "best_score": 0,
            "comparison": []
        }
        
        for name, model in self.models.items():
            # Train
            model.fit(self.X_train, self.y_train)
            
            # Predict
            y_pred_train = model.predict(self.X_train)
            y_pred_test = model.predict(self.X_test)
            
            # Get probabilities
            y_proba_test = model.predict_proba(self.X_test)
            
            # Evaluate
            metrics = {
                "train_accuracy": float(accuracy_score(self.y_train, y_pred_train)),
                "test_accuracy": float(accuracy_score(self.y_test, y_pred_test)),
                "precision": float(precision_score(self.y_test, y_pred_test, average='weighted', zero_division=0)),
                "recall": float(recall_score(self.y_test, y_pred_test, average='weighted', zero_division=0)),
                "f1_score": float(f1_score(self.y_test, y_pred_test, average='weighted', zero_division=0)),
                "confusion_matrix": confusion_matrix(self.y_test, y_pred_test).tolist()
            }
            
            # Store results
            results["models"][name] = {
                "metrics": metrics,
                "predictions": y_pred_test.tolist()[:10],  # First 10 predictions
                "probabilities": y_proba_test.tolist()[:10],  # First 10 probabilities
                "model_type": name
            }
            
            # Track best model
            if metrics["test_accuracy"] > results["best_score"]:
                results["best_score"] = metrics["test_accuracy"]
                results["best_model"] = name
                self.best_model = model
                self.best_model_name = name
            
            # Add to comparison
            results["comparison"].append({
                "model": name,
                "accuracy": metrics["test_accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"]
            })
        
        # Sort comparison by accuracy
        results["comparison"].sort(key=lambda x: x["accuracy"], reverse=True)
        
        # Add interpretation
        results["interpretation"] = self._interpret_results(results)
        
        return results
    
    def _interpret_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate interpretation of model results"""
        best_model = results["best_model"]
        best_metrics = results["models"][best_model]["metrics"]
        
        interpretation = {
            "summary": (
                f"{best_model} performs best with {best_metrics['test_accuracy']:.2%} accuracy. "
                f"This model provides a good balance between accuracy and interpretability."
            ),
            "confidence_level": self._assess_confidence(best_metrics),
            "reliability": self._assess_reliability(best_metrics)
        }
        
        return interpretation
    
    def _assess_confidence(self, metrics: Dict[str, float]) -> str:
        """Assess model confidence based on metrics"""
        accuracy = metrics["test_accuracy"]
        
        if accuracy >= 0.9:
            return "Very High"
        elif accuracy >= 0.8:
            return "High"
        elif accuracy >= 0.7:
            return "Moderate"
        elif accuracy >= 0.6:
            return "Low"
        else:
            return "Very Low"
    
    def _assess_reliability(self, metrics: Dict[str, float]) -> str:
        """Assess model reliability"""
        train_acc = metrics["train_accuracy"]
        test_acc = metrics["test_accuracy"]
        
        # Check for overfitting
        if train_acc - test_acc > 0.15:
            return "Potential overfitting detected - use with caution"
        elif train_acc - test_acc < 0.05:
            return "Good generalization - reliable predictions"
        else:
            return "Moderate generalization - reasonable reliability"
    
    def predict_with_probability(self, X: pd.DataFrame) -> Dict[str, Any]:
        """Make predictions with probability scores"""
        if self.best_model is None:
            raise ValueError("No model trained yet")
        
        predictions = self.best_model.predict(X)
        probabilities = self.best_model.predict_proba(X)
        
        return {
            "predictions": predictions.tolist(),
            "probabilities": probabilities.tolist(),
            "model_used": self.best_model_name
        }
