"""
NEXORA AI - FastAPI Backend Server
Main entry point for the Decision Intelligence System
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import os
import json

from backend.data_processor import DataProcessor
from backend.eda_analyzer import EDAAnalyzer
from backend.ml_model import MLModelEngine
from backend.explainer import ExplainerEngine
from backend.decision_intelligence import DecisionIntelligence

# Initialize FastAPI app
app = FastAPI(
    title="NEXORA AI - Decision Intelligence System",
    description="Explainable Decision Intelligence System using Classical ML",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Global state (in production, use a database)
session_data = {}

# Pydantic models for request/response
class DecisionContext(BaseModel):
    decision_type: str
    description: str
    domain: Optional[str] = "general"

class DataInput(BaseModel):
    data: Dict[str, Any]
    features: List[str]
    target: Optional[str] = None

class ValidationFeedback(BaseModel):
    decision: str  # "accept", "modify", "reject"
    comments: Optional[str] = None
    modified_recommendation: Optional[str] = None
    confidence: Optional[int] = None

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint - serve main page"""
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "NEXORA AI - Decision Intelligence System API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "NEXORA AI"}

@app.post("/api/decision-context")
async def set_decision_context(context: DecisionContext):
    """Step 1: Set decision context"""
    session_id = "default"  # In production, generate unique session IDs
    session_data[session_id] = {
        "context": context.dict(),
        "step": 1
    }
    return {
        "status": "success",
        "message": "Decision context saved",
        "session_id": session_id,
        "context": context.dict()
    }

@app.post("/api/upload-data")
async def upload_data(file: UploadFile = File(...)):
    """Step 2: Upload CSV data"""
    try:
        processor = DataProcessor()
        data_info = await processor.process_upload(file)
        
        session_id = "default"
        if session_id not in session_data:
            session_data[session_id] = {}
        
        session_data[session_id]["raw_data"] = data_info
        session_data[session_id]["step"] = 2
        
        # Don't return DataFrame in response, only metadata
        response_info = {k: v for k, v in data_info.items() if k != 'dataframe'}
        
        return {
            "status": "success",
            "message": "Data uploaded successfully",
            "data_info": response_info
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/preprocess")
async def preprocess_data():
    """Step 3: Preprocess data"""
    session_id = "default"
    if session_id not in session_data or "raw_data" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No data uploaded")
    
    try:
        processor = DataProcessor()
        raw_data = session_data[session_id]["raw_data"]
        preprocessed = processor.preprocess(raw_data["dataframe"])
        
        session_data[session_id]["preprocessed_data"] = preprocessed
        session_data[session_id]["step"] = 3
        
        return {
            "status": "success",
            "message": "Data preprocessed successfully",
            "preprocessing_report": preprocessed["report"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/eda")
async def perform_eda():
    """Step 4: Perform Exploratory Data Analysis"""
    session_id = "default"
    if session_id not in session_data or "preprocessed_data" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No preprocessed data available")
    
    try:
        analyzer = EDAAnalyzer()
        df = session_data[session_id]["preprocessed_data"]["dataframe"]
        eda_results = analyzer.analyze(df)
        
        session_data[session_id]["eda_results"] = eda_results
        session_data[session_id]["step"] = 4
        
        return {
            "status": "success",
            "message": "EDA completed successfully",
            "eda_results": eda_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train-model")
async def train_model(data_input: DataInput):
    """Step 5 & 6: Train ML model"""
    session_id = "default"
    if session_id not in session_data or "preprocessed_data" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No preprocessed data available")
    
    try:
        ml_engine = MLModelEngine()
        df = session_data[session_id]["preprocessed_data"]["dataframe"]
        
        # Train models
        model_results = ml_engine.train_and_evaluate(
            df,
            data_input.features,
            data_input.target
        )
        
        session_data[session_id]["model_results"] = model_results
        session_data[session_id]["ml_engine"] = ml_engine
        session_data[session_id]["step"] = 6
        
        return {
            "status": "success",
            "message": "Model trained successfully",
            "model_results": model_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/explain")
async def explain_predictions():
    """Step 7: Generate Explainable AI insights"""
    session_id = "default"
    if session_id not in session_data or "model_results" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No model results available")
    
    try:
        explainer = ExplainerEngine()
        ml_engine = session_data[session_id]["ml_engine"]
        df = session_data[session_id]["preprocessed_data"]["dataframe"]
        
        explanations = explainer.generate_explanations(
            ml_engine.best_model,
            ml_engine.X_test,
            ml_engine.y_test,
            ml_engine.feature_names
        )
        
        session_data[session_id]["explanations"] = explanations
        session_data[session_id]["step"] = 7
        
        return {
            "status": "success",
            "message": "Explanations generated successfully",
            "explanations": explanations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recommendations")
async def generate_recommendations():
    """Step 8: Generate decision recommendations"""
    session_id = "default"
    if session_id not in session_data or "explanations" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No explanations available")
    
    try:
        di_engine = DecisionIntelligence()
        
        recommendations = di_engine.generate_recommendations(
            session_data[session_id]["model_results"],
            session_data[session_id]["explanations"]
        )
        
        session_data[session_id]["recommendations"] = recommendations
        session_data[session_id]["step"] = 8
        
        return {
            "status": "success",
            "message": "Recommendations generated successfully",
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate")
async def validate_decision(feedback: ValidationFeedback):
    """Step 9: Human validation"""
    session_id = "default"
    if session_id not in session_data or "recommendations" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No recommendations available")
    
    try:
        di_engine = DecisionIntelligence()
        
        validation_result = di_engine.process_validation(
            feedback.dict(),
            session_data[session_id]["recommendations"]
        )
        
        session_data[session_id]["validation"] = validation_result
        session_data[session_id]["step"] = 9
        
        return {
            "status": "success",
            "message": "Validation recorded successfully",
            "validation_result": validation_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/decision-quality")
async def get_decision_quality():
    """Step 10: Decision quality metrics"""
    session_id = "default"
    if session_id not in session_data or "validation" not in session_data[session_id]:
        raise HTTPException(status_code=400, detail="No validation data available")
    
    try:
        di_engine = DecisionIntelligence()
        
        quality_metrics = di_engine.calculate_quality_metrics(
            session_data[session_id]["validation"],
            session_data[session_id]["model_results"]
        )
        
        session_data[session_id]["quality_metrics"] = quality_metrics
        session_data[session_id]["step"] = 10
        
        return {
            "status": "success",
            "message": "Quality metrics calculated successfully",
            "quality_metrics": quality_metrics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session-state")
async def get_session_state():
    """Get current session state"""
    session_id = "default"
    if session_id not in session_data:
        return {"status": "no_session", "step": 0}
    
    return {
        "status": "active",
        "step": session_data[session_id].get("step", 0),
        "has_context": "context" in session_data[session_id],
        "has_data": "raw_data" in session_data[session_id],
        "has_preprocessed": "preprocessed_data" in session_data[session_id],
        "has_model": "model_results" in session_data[session_id]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
