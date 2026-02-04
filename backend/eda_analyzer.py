"""
EDA Analyzer Module
Performs Exploratory Data Analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

class EDAAnalyzer:
    """Perform comprehensive EDA on datasets"""
    
    def __init__(self):
        pass
    
    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform complete EDA
        Returns: Dictionary with analysis results
        """
        results = {
            "statistical_summary": self._statistical_summary(df),
            "correlation_analysis": self._correlation_analysis(df),
            "distribution_insights": self._distribution_insights(df),
            "feature_insights": self._feature_insights(df),
            "key_observations": []
        }
        
        # Generate key observations
        results["key_observations"] = self._generate_observations(results)
        
        return results
    
    def _statistical_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate statistical summary for numeric columns"""
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) == 0:
            return {"message": "No numeric columns found"}
        
        summary = {}
        for col in numeric_cols:
            summary[col] = {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "q25": float(df[col].quantile(0.25)),
                "q75": float(df[col].quantile(0.75)),
                "skewness": float(df[col].skew()),
                "kurtosis": float(df[col].kurtosis())
            }
        
        return summary
    
    def _correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between numeric features"""
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        if len(numeric_cols) < 2:
            return {"message": "Need at least 2 numeric columns for correlation"}
        
        # Calculate correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Find strong correlations (|r| > 0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    strong_correlations.append({
                        "feature1": corr_matrix.columns[i],
                        "feature2": corr_matrix.columns[j],
                        "correlation": float(corr_val),
                        "strength": "strong positive" if corr_val > 0 else "strong negative"
                    })
        
        return {
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations,
            "interpretation": "Correlations show linear relationships between features"
        }
    
    def _distribution_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze distributions of features"""
        insights = {}
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        
        for col in numeric_cols:
            # Check for normality (simple heuristic)
            skew = df[col].skew()
            
            if abs(skew) < 0.5:
                distribution_type = "approximately normal"
            elif skew > 0:
                distribution_type = "right-skewed (positive skew)"
            else:
                distribution_type = "left-skewed (negative skew)"
            
            insights[col] = {
                "distribution_type": distribution_type,
                "skewness": float(skew),
                "range": float(df[col].max() - df[col].min()),
                "variance": float(df[col].var())
            }
        
        return insights
    
    def _feature_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate insights about individual features"""
        insights = {}
        
        for col in df.columns:
            col_insights = {
                "unique_values": int(df[col].nunique()),
                "missing_percentage": float(df[col].isnull().sum() / len(df) * 100),
                "data_type": str(df[col].dtype)
            }
            
            # Feature type classification
            if df[col].dtype in ['float64', 'int64']:
                if df[col].nunique() <= 10:
                    col_insights["feature_type"] = "discrete numeric"
                else:
                    col_insights["feature_type"] = "continuous numeric"
            else:
                if df[col].nunique() <= 5:
                    col_insights["feature_type"] = "binary/categorical"
                else:
                    col_insights["feature_type"] = "multi-class categorical"
            
            insights[col] = col_insights
        
        return insights
    
    def _generate_observations(self, results: Dict[str, Any]) -> List[str]:
        """Generate key observations from EDA results"""
        observations = []
        
        # Observation from correlations
        if "strong_correlations" in results["correlation_analysis"]:
            strong_corrs = results["correlation_analysis"]["strong_correlations"]
            if strong_corrs:
                observations.append(
                    f"Found {len(strong_corrs)} strong correlations between features, "
                    "indicating potential relationships that can be leveraged for prediction."
                )
        
        # Observation from distributions
        if results["distribution_insights"]:
            skewed_features = [
                col for col, info in results["distribution_insights"].items()
                if abs(info["skewness"]) > 1.0
            ]
            if skewed_features:
                observations.append(
                    f"Features {skewed_features} show significant skewness, "
                    "which may require transformation for optimal model performance."
                )
        
        # General observation
        observations.append(
            "Data exploration complete. Features are ready for model training with "
            "appropriate preprocessing applied."
        )
        
        return observations
