from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
import uuid
from datetime import datetime
from bson import ObjectId
from app.models.dpr import DPRCreate, DPRResponse, FileType, DPRExtraction
from app.models.risk import RiskCreate, RiskScore
from app.utils.dpr_processor import extract_text_from_pdf, extract_text_from_word, extract_text_from_image, extract_dpr_elements
from app.database import get_dprs_collection, get_risks_collection
from app.services.risk_calculator import calculate_risk_scores
from app.ai.ai_service import AIService
from app.models.ai_models import EnhancedDPRExtraction
import os

router = APIRouter()
ai_service = AIService()

@router.get("/reports/{report_filename}")
async def download_report(report_filename: str):
    """Download a generated report PDF"""
    # Check if file exists in backend directory (where reports are generated)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(backend_dir, report_filename)
    
    # Also check in current directory as fallback
    if not os.path.exists(file_path):
        file_path = os.path.join(os.getcwd(), report_filename)
    
    # Also check in the root directory
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(backend_dir), report_filename)
    
    print(f"Looking for report file: {file_path}")
    
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

@router.post("/upload", response_model=DPRResponse)
async def upload_dpr(
    file: UploadFile = File(...),
    uploaded_by: str = Form(...)
):
    dprs_collection = get_dprs_collection()
    
    # Determine file type
    file_type = None
    if file.content_type == "application/pdf":
        file_type = FileType.PDF
    elif file.content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        file_type = FileType.WORD
    elif file.content_type.startswith("image/"):
        file_type = FileType.IMAGE
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload PDF, Word, or image files."
        )
    
    # Read file content
    file_content = await file.read()
    
    # Extract text based on file type
    if file_type == FileType.PDF:
        text = extract_text_from_pdf(file_content)
    elif file_type == FileType.WORD:
        text = extract_text_from_word(file_content)
    elif file_type == FileType.IMAGE:
        text = extract_text_from_image(file_content)
    
    # Extract DPR elements using AI service (which now uses specialized extraction)
    enhanced_extraction = ai_service.extract_dpr_entities(text)
    
    # Convert to DPRExtraction format for compatibility
    extracted_data = DPRExtraction(
        project_title=enhanced_extraction.project_title,
        budget=enhanced_extraction.budget,
        timeline=enhanced_extraction.timeline,
        resource_allocation=enhanced_extraction.resource_allocation,
        location=enhanced_extraction.location,
        environmental_risks=enhanced_extraction.environmental_risks,
        technical_sections=enhanced_extraction.technical_sections
    )
    
    # Create DPR document
    dpr_doc = {
        "file_name": file.filename,
        "file_type": file_type,
        "uploaded_by": uploaded_by,
        "extracted_data": extracted_data.dict(),
        "uploaded_at": datetime.utcnow()
    }
    
    # Insert DPR into database
    result = dprs_collection.insert_one(dpr_doc)
    dpr_doc["id"] = str(result.inserted_id)
    
    # Calculate and store risk scores using enhanced extraction
    risk_scores = calculate_risk_scores(extracted_data)
    risk_doc = {
        "dpr_id": dpr_doc["id"],
        "project_title": enhanced_extraction.project_title or "Unknown Project",
        "calculated_at": datetime.utcnow(),
        "risk_scores": risk_scores.dict()
    }
    
    risks_collection = get_risks_collection()
    risks_collection.insert_one(risk_doc)
    
    return dpr_doc

@router.post("/upload_with_ai", response_model=dict)
async def upload_dpr_with_ai(
    file: UploadFile = File(...),
    uploaded_by: str = Form(...),
    generate_reports: bool = Form(default=True)
):
    """
    Upload DPR with full AI analysis
    """
    dprs_collection = get_dprs_collection()
    
    # Determine file type
    file_type = None
    if file.content_type == "application/pdf":
        file_type = FileType.PDF
    elif file.content_type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        file_type = FileType.WORD
    elif file.content_type.startswith("image/"):
        file_type = FileType.IMAGE
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload PDF, Word, or image files."
        )
    
    # Read file content
    file_content = await file.read()
    
    # Extract text based on file type
    if file_type == FileType.PDF:
        text = extract_text_from_pdf(file_content)
    elif file_type == FileType.WORD:
        text = extract_text_from_word(file_content)
    elif file_type == FileType.IMAGE:
        text = extract_text_from_image(file_content)
    
    # Extract enhanced entities using AI (which now uses specialized extraction)
    enhanced_extraction = ai_service.extract_dpr_entities(text)
    
    # Calculate completeness score
    completeness_score = ai_service.calculate_completeness_score(enhanced_extraction)
    
    # Convert to DPRExtraction format for compatibility
    extracted_data = DPRExtraction(
        project_title=enhanced_extraction.project_title,
        budget=enhanced_extraction.budget,
        timeline=enhanced_extraction.timeline,
        resource_allocation=enhanced_extraction.resource_allocation,
        location=enhanced_extraction.location,
        environmental_risks=enhanced_extraction.environmental_risks,
        technical_sections=enhanced_extraction.technical_sections
    )
    
    # AI Analysis
    ai_risk_scores = ai_service.predict_dpr_risks(enhanced_extraction)
    recommendations = ai_service.generate_recommendations(ai_risk_scores, completeness_score)
    
    # Create DPR document
    dpr_doc = {
        "file_name": file.filename,
        "file_type": file_type,
        "uploaded_by": uploaded_by,
        "extracted_data": extracted_data.dict(),
        "enhanced_extraction": enhanced_extraction.dict(),
        "completeness_score": completeness_score,
        "original_text": text,  # Store original text for future analysis
        "uploaded_at": datetime.utcnow()
    }
    
    # Insert DPR into database
    result = dprs_collection.insert_one(dpr_doc)
    dpr_id = str(result.inserted_id)
    dpr_doc["id"] = dpr_id
    # Remove the MongoDB _id field to avoid serialization issues
    if "_id" in dpr_doc:
        del dpr_doc["_id"]
    
    # Store risk scores
    risk_doc = {
        "dpr_id": dpr_id,
        "project_title": enhanced_extraction.project_title or "Unknown Project",
        "calculated_at": datetime.utcnow(),
        "risk_scores": ai_risk_scores
    }
    
    risks_collection = get_risks_collection()
    risks_collection.insert_one(risk_doc)
    
    # Generate reports if requested
    report_files = {}
    if generate_reports:
        analytical_report = ai_service.generate_analytical_report(
            dpr_id, enhanced_extraction, ai_risk_scores, recommendations
        )
        recommendation_report = ai_service.generate_recommendation_report(
            dpr_id, enhanced_extraction, ai_risk_scores, recommendations
        )
        report_files = {
            "analytical_report": analytical_report,
            "recommendation_report": recommendation_report
        }
        
        # Update DPR document with report information
        dprs_collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"reports": report_files}}
        )
    
    return {
        "dpr": dpr_doc,
        "ai_risk_scores": ai_risk_scores,
        "recommendations": [rec.dict() for rec in recommendations],
        "completeness_score": completeness_score,
        "reports": report_files
    }

@router.get("/{dpr_id}", response_model=DPRResponse)
async def get_dpr(dpr_id: str):
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    dpr["id"] = str(dpr["_id"])
    del dpr["_id"]
    
    return dpr

@router.get("/user/{user_id}", response_model=List[DPRResponse])
async def get_user_dprs(user_id: str):
    dprs_collection = get_dprs_collection()
    
    # Find all DPRs uploaded by user
    dprs = list(dprs_collection.find({"uploaded_by": user_id}))
    
    # Format response
    for dpr in dprs:
        dpr["id"] = str(dpr["_id"])
        del dpr["_id"]
    
    return dprs

@router.post("/{dpr_id}/analyze_with_ai", response_model=dict)
async def analyze_dpr_with_ai(dpr_id: str):
    """
    Perform full AI analysis on an existing DPR
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Get the original text content from the DPR if available
    # Otherwise recreate from extracted data
    text_content = dpr.get("original_text", "")
    
    if not text_content:
        # Recreate text from extracted data as fallback
        extracted_data = dpr.get("extracted_data", {})
        for key, value in extracted_data.items():
            if value:
                text_content += f"{key}: {value}\n"
    
    # Extract enhanced entities using AI
    enhanced_extraction = ai_service.extract_dpr_entities(text_content)
    
    # Calculate completeness score
    completeness_score = ai_service.calculate_completeness_score(enhanced_extraction)
    
    # AI Analysis
    ai_risk_scores = ai_service.predict_dpr_risks(enhanced_extraction)
    recommendations = ai_service.generate_recommendations(ai_risk_scores, completeness_score)
    
    # Generate reports
    analytical_report = ai_service.generate_analytical_report(
        dpr_id, enhanced_extraction, ai_risk_scores, recommendations
    )
    recommendation_report = ai_service.generate_recommendation_report(
        dpr_id, enhanced_extraction, ai_risk_scores, recommendations
    )
    
    # Update DPR document with AI analysis results
    dprs_collection.update_one(
        {"_id": ObjectId(dpr_id)},
        {"$set": {
            "enhanced_extraction": enhanced_extraction.dict(),
            "ai_risk_scores": ai_risk_scores,
            "recommendations": [rec.dict() for rec in recommendations],
            "completeness_score": completeness_score
        }}
    )
    
    return {
        "dpr_id": dpr_id,
        "enhanced_extraction": enhanced_extraction.dict(),
        "ai_risk_scores": ai_risk_scores,
        "recommendations": [rec.dict() for rec in recommendations],
        "completeness_score": completeness_score,
        "reports": {
            "analytical_report": analytical_report,
            "recommendation_report": recommendation_report
        }
    }

@router.get("/{dpr_id}/completeness", response_model=dict)
async def get_dpr_completeness(dpr_id: str):
    """
    Get completeness score for a DPR
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Check if completeness score already exists
    completeness_score = dpr.get("completeness_score")
    
    if completeness_score is None:
        # Calculate completeness score
        enhanced_extraction_data = dpr.get("enhanced_extraction", {})
        if enhanced_extraction_data:
            from app.models.ai_models import EnhancedDPRExtraction
            try:
                enhanced_extraction = EnhancedDPRExtraction(**enhanced_extraction_data)
                completeness_score = ai_service.calculate_completeness_score(enhanced_extraction)
                
                # Update DPR with completeness score
                dprs_collection.update_one(
                    {"_id": ObjectId(dpr_id)},
                    {"$set": {"completeness_score": completeness_score}}
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error calculating completeness score: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="DPR has not been analyzed with AI yet. Please run AI analysis first."
            )
    
    return {
        "dpr_id": dpr_id,
        "completeness_score": completeness_score
    }

@router.get("/organization/dashboard", response_model=List[DPRResponse])
async def get_all_dprs_for_organization():
    """
    Get all DPRs for organization dashboard
    """
    dprs_collection = get_dprs_collection()
    risks_collection = get_risks_collection()
    
    # Find all DPRs
    dprs = list(dprs_collection.find({}))
    
    # Format response with error handling
    formatted_dprs = []
    for dpr in dprs:
        try:
            dpr["id"] = str(dpr["_id"])
            del dpr["_id"]
            
            # Ensure all necessary fields are present for dashboard display
            if "enhanced_extraction" not in dpr:
                dpr["enhanced_extraction"] = {}
                
            # Get AI risk scores from risks collection if not in DPR
            if "ai_risk_scores" not in dpr or not dpr["ai_risk_scores"]:
                risk_record = risks_collection.find_one({"dpr_id": dpr["id"]})
                if risk_record and "risk_scores" in risk_record:
                    dpr["ai_risk_scores"] = risk_record["risk_scores"]
                else:
                    dpr["ai_risk_scores"] = {}
                    
            if "completeness_score" not in dpr:
                dpr["completeness_score"] = 0
            
            # Remove any fields that might cause serialization issues
            if "original_text" in dpr and len(str(dpr.get("original_text", ""))) > 100000:
                # Truncate very large text fields
                dpr["original_text"] = str(dpr["original_text"])[:100000] + "... [truncated]"
            
            formatted_dprs.append(dpr)
        except Exception as e:
            # Log the error but continue processing other DPRs
            print(f"Error processing DPR {dpr.get('_id', 'unknown')}: {str(e)}")
            continue
    
    # Sort by upload date (newest first)
    # Handle both string and datetime types
    def get_sort_key(dpr):
        try:
            uploaded_at = dpr.get("uploaded_at", datetime.min)
            if isinstance(uploaded_at, str):
                try:
                    # Try ISO format first
                    return datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                except:
                    return datetime.min
            return uploaded_at if uploaded_at else datetime.min
        except:
            return datetime.min
    
    formatted_dprs.sort(key=get_sort_key, reverse=True)
    
    return formatted_dprs

@router.delete("/{dpr_id}", response_model=dict)
async def delete_dpr(dpr_id: str):
    """
    Delete a DPR by ID
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Delete the DPR
    result = dprs_collection.delete_one({"_id": ObjectId(dpr_id)})
    
    if result.deleted_count == 1:
        return {"message": "DPR deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete DPR"
        )

@router.post("/{dpr_id}/approve", response_model=dict)
async def approve_dpr(dpr_id: str):
    """
    Approve a DPR by ID
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Update the DPR with approved status
    dprs_collection.update_one(
        {"_id": ObjectId(dpr_id)},
        {"$set": {"approved": True, "approved_at": datetime.utcnow()}}
    )
    
    return {"message": "DPR approved successfully"}
