"""
Data Processor Module
Handles data upload, validation, cleaning, and preprocessing
"""

import pandas as pd
import numpy as np
from io import StringIO
from typing import Dict, Any
from fastapi import UploadFile

class DataProcessor:
    """Handle all data preprocessing operations"""
    
    def __init__(self):
        self.df = None
        
    async def process_upload(self, file: UploadFile) -> Dict[str, Any]:
        """
        Process uploaded CSV file
        Returns: Dictionary with data information
        """
        contents = await file.read()
        csv_string = contents.decode('utf-8')
        
        # Parse CSV
        df = pd.read_csv(StringIO(csv_string))
        
        # Basic validation
        if df.empty:
            raise ValueError("Uploaded file is empty")
        
        # Store dataframe
        self.df = df
        
        # Generate data info
        info = {
            "filename": file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "column_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(5).to_dict(orient='records'),
            "dataframe": df  # Store for later use
        }
        
        return info
    
    def preprocess(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Preprocess data: handle missing values, encode categorical, normalize
        Returns: Dictionary with preprocessed dataframe and report
        """
        report = {
            "steps_performed": [],
            "issues_found": [],
            "transformations": {}
        }
        
        df_processed = df.copy()
        
        # 1. Handle missing values
        missing_cols = df_processed.columns[df_processed.isnull().any()].tolist()
        if missing_cols:
            report["issues_found"].append(f"Missing values in columns: {missing_cols}")
            
            for col in missing_cols:
                if df_processed[col].dtype in ['float64', 'int64']:
                    # Fill numeric with median
                    median_val = df_processed[col].median()
                    df_processed[col].fillna(median_val, inplace=True)
                    report["transformations"][col] = f"Filled with median: {median_val}"
                else:
                    # Fill categorical with mode
                    mode_val = df_processed[col].mode()[0] if not df_processed[col].mode().empty else 'Unknown'
                    df_processed[col].fillna(mode_val, inplace=True)
                    report["transformations"][col] = f"Filled with mode: {mode_val}"
            
            report["steps_performed"].append("Missing value imputation")
        
        # 2. Encode categorical variables
        categorical_cols = df_processed.select_dtypes(include=['object']).columns.tolist()
        if categorical_cols:
            report["steps_performed"].append("Categorical encoding")
            
            for col in categorical_cols:
                # Simple label encoding for now
                unique_vals = df_processed[col].unique()
                if len(unique_vals) <= 10:  # Only encode if reasonable number of categories
                    df_processed[col] = pd.Categorical(df_processed[col]).codes
                    report["transformations"][col] = f"Label encoded ({len(unique_vals)} categories)"
        
        # 3. Check for outliers (basic IQR method)
        numeric_cols = df_processed.select_dtypes(include=['float64', 'int64']).columns.tolist()
        outlier_info = {}
        
        for col in numeric_cols:
            Q1 = df_processed[col].quantile(0.25)
            Q3 = df_processed[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df_processed[col] < (Q1 - 1.5 * IQR)) | 
                       (df_processed[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                outlier_info[col] = int(outliers)
        
        if outlier_info:
            report["issues_found"].append(f"Outliers detected: {outlier_info}")
        
        # 4. Data quality summary
        report["final_shape"] = df_processed.shape
        report["data_quality"] = {
            "completeness": float(1 - df_processed.isnull().sum().sum() / (df_processed.shape[0] * df_processed.shape[1])),
            "numeric_features": len(numeric_cols),
            "categorical_features": len(categorical_cols)
        }
        
        return {
            "dataframe": df_processed,
            "report": report,
            "original_shape": df.shape,
            "processed_shape": df_processed.shape
        }
    
    def get_feature_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get detailed feature information"""
        info = {}
        
        for col in df.columns:
            col_info = {
                "type": str(df[col].dtype),
                "missing": int(df[col].isnull().sum()),
                "unique": int(df[col].nunique())
            }
            
            if df[col].dtype in ['float64', 'int64']:
                col_info.update({
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max())
                })
            
            info[col] = col_info
        
        return info
