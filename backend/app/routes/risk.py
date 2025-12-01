from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime
from app.models.risk import RiskCreate, RiskResponse, RiskScore
from app.database import get_risks_collection, get_dprs_collection
from app.ai.ai_service import AIService
from app.models.ai_models import EnhancedDPRExtraction

router = APIRouter()
ai_service = AIService()

@router.get("/{dpr_id}", response_model=RiskResponse)
async def get_risk_assessment(dpr_id: str):
    """Get risk assessment for a DPR"""
    risks_collection = get_risks_collection()
    
    # Find risk assessment by DPR ID
    risk_doc = risks_collection.find_one({"dpr_id": dpr_id})
    if not risk_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    
    risk_doc["id"] = str(risk_doc["_id"])
    del risk_doc["_id"]
    
    return risk_doc

@router.post("/assess_with_ai/{dpr_id}", response_model=dict)
async def assess_risk_with_ai(dpr_id: str):
    """
    Perform AI-powered risk assessment for a DPR
    """
    dprs_collection = get_dprs_collection()
    risks_collection = get_risks_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Get enhanced extraction data
    enhanced_extraction_data = dpr.get("enhanced_extraction")
    if not enhanced_extraction_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DPR has not been analyzed with AI yet. Please run AI analysis first."
        )
    
    # Deserialize enhanced extraction
    try:
        enhanced_extraction = EnhancedDPRExtraction(**enhanced_extraction_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deserializing enhanced extraction: {str(e)}"
        )
    
    # Predict risks using AI
    ai_risk_scores = ai_service.predict_dpr_risks(enhanced_extraction)
    
    # Calculate completeness score
    completeness_score = ai_service.calculate_completeness_score(enhanced_extraction)
    
    # Generate recommendations
    recommendations = ai_service.generate_recommendations(ai_risk_scores, completeness_score)
    
    # Update risk assessment in database
    risk_doc = {
        "dpr_id": dpr_id,
        "project_title": enhanced_extraction.project_title or "Unknown Project",
        "calculated_at": datetime.utcnow(),
        "risk_scores": ai_risk_scores,
        "completeness_score": completeness_score,
        "recommendations": [rec.dict() for rec in recommendations]
    }
    
    # Check if risk assessment already exists
    existing_risk = risks_collection.find_one({"dpr_id": dpr_id})
    if existing_risk:
        # Update existing risk assessment
        risks_collection.update_one(
            {"dpr_id": dpr_id},
            {"$set": risk_doc}
        )
    else:
        # Create new risk assessment
        risks_collection.insert_one(risk_doc)
    
    # Update DPR with AI analysis results
    dprs_collection.update_one(
        {"_id": ObjectId(dpr_id)},
        {"$set": {
            "ai_risk_scores": ai_risk_scores,
            "recommendations": [rec.dict() for rec in recommendations],
            "completeness_score": completeness_score
        }}
    )
    
    return {
        "dpr_id": dpr_id,
        "risk_scores": ai_risk_scores,
        "completeness_score": completeness_score,
        "recommendations": [rec.dict() for rec in recommendations]
    }

@router.get("/visualize/{dpr_id}", response_model=dict)
async def visualize_risks(dpr_id: str):
    """
    Get risk data for visualization
    """
    risks_collection = get_risks_collection()
    
    # Find risk assessment by DPR ID
    risk_doc = risks_collection.find_one({"dpr_id": dpr_id})
    if not risk_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found"
        )
    
    # Prepare data for visualization
    risk_scores = risk_doc.get("risk_scores", {})
    
    # Convert to format suitable for charts
    labels = list(risk_scores.keys())
    values = list(risk_scores.values())
    
    return {
        "labels": labels,
        "values": values
    }