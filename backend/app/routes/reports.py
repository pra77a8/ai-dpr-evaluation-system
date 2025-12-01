from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from bson import ObjectId
from app.ai.ai_service import AIService
from app.database import get_dprs_collection
from app.models.ai_models import EnhancedDPRExtraction, Recommendation
import os

router = APIRouter()
ai_service = AIService()

class ReportRequest(BaseModel):
    dpr_id: str
    report_type: str  # "analytical" or "recommendation"

class ReportResponse(BaseModel):
    message: str
    report_path: str

@router.post("/generate", response_model=ReportResponse)
async def generate_report(report_request: ReportRequest):
    """
    Generate AI-powered reports for a DPR
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(report_request.dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Get enhanced extraction
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
    
    # Get AI analysis results
    ai_risk_scores = dpr.get("ai_risk_scores")
    recommendations_data = dpr.get("recommendations", [])
    
    if not ai_risk_scores:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DPR has not been analyzed with AI yet. Please run AI analysis first."
        )
    
    recommendations = []
    for rec_data in recommendations_data:
        try:
            rec = Recommendation(**rec_data)
            recommendations.append(rec)
        except:
            pass
    
    # Generate report based on type
    if report_request.report_type == "analytical":
        report_filename = ai_service.generate_analytical_report(
            report_request.dpr_id, enhanced_extraction, ai_risk_scores, recommendations
        )
    elif report_request.report_type == "recommendation":
        report_filename = ai_service.generate_recommendation_report(
            report_request.dpr_id, enhanced_extraction, ai_risk_scores, recommendations
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid report type. Use 'analytical' or 'recommendation'."
        )
    
    # Update DPR with report information
    reports = dpr.get("reports", {})
    if report_request.report_type == "analytical":
        reports["analytical_report"] = report_filename
    else:
        reports["recommendation_report"] = report_filename
    
    dprs_collection.update_one(
        {"_id": ObjectId(report_request.dpr_id)},
        {"$set": {"reports": reports}}
    )
    
    return ReportResponse(
        message=f"{report_request.report_type.capitalize()} report generated successfully",
        report_path=report_filename
    )

@router.get("/download/{report_filename}")
async def download_report(report_filename: str):
    """
    Download a generated report
    """
    # Check if file exists in backend directory
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(backend_dir, report_filename)
    
    # Also check in current directory as fallback
    if not os.path.exists(file_path):
        file_path = os.path.join(os.getcwd(), report_filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report not found: {report_filename}"
        )
    
    return FileResponse(
        path=file_path,
        filename=report_filename,
        media_type='application/pdf'
    )