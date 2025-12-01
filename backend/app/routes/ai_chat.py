from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId
from app.ai.ai_service import AIService
from app.database import get_dprs_collection
from datetime import datetime
import json

router = APIRouter()
ai_service = AIService()

class ChatRequest(BaseModel):
    question: str
    dpr_id: str

class ChatResponse(BaseModel):
    answer: str
    dpr_id: str
    timestamp: datetime

# Add the translation request model
class TranslationRequest(BaseModel):
    text: str
    target_lang: str

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_dpr(chat_request: ChatRequest):
    """
    Chat with DPR using AI-powered chatbot
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(chat_request.dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Get enhanced extraction if available, otherwise use basic extraction
    enhanced_extraction_data = dpr.get("enhanced_extraction")
    if not enhanced_extraction_data:
        # Fallback to basic extraction
        enhanced_extraction_data = dpr.get("extracted_data", {})
    
    # For now, we'll create a simple extraction object
    # In a real implementation, you would properly deserialize this
    from app.models.ai_models import EnhancedDPRExtraction
    try:
        enhanced_extraction = EnhancedDPRExtraction(**enhanced_extraction_data)
    except:
        # Create a basic extraction if deserialization fails
        enhanced_extraction = EnhancedDPRExtraction(
            project_title=enhanced_extraction_data.get("project_title"),
            budget=enhanced_extraction_data.get("budget"),
            timeline=enhanced_extraction_data.get("timeline"),
            resource_allocation=enhanced_extraction_data.get("resource_allocation"),
            location=enhanced_extraction_data.get("location"),
            environmental_risks=enhanced_extraction_data.get("environmental_risks")
        )
    
    # Get AI analysis results if available
    ai_risk_scores = dpr.get("ai_risk_scores")
    recommendations_data = dpr.get("recommendations", [])
    
    # If not available, use default values
    if not ai_risk_scores:
        ai_risk_scores = {
            "cost_overruns": 0.5,
            "schedule_delays": 0.5,
            "resource_shortages": 0.5,
            "environmental_risks": 0.5
        }
    
    from app.models.ai_models import Recommendation
    recommendations = []
    for rec_data in recommendations_data:
        try:
            rec = Recommendation(**rec_data)
            recommendations.append(rec)
        except:
            pass
    
    # Answer the question using the chatbot
    answer = ai_service.answer_dpr_question(
        chat_request.question, enhanced_extraction, ai_risk_scores, recommendations
    )
    
    return ChatResponse(
        answer=answer,
        dpr_id=chat_request.dpr_id,
        timestamp=datetime.utcnow()
    )

@router.post("/chat_advanced", response_model=ChatResponse)
async def chat_with_dpr_advanced(chat_request: ChatRequest):
    """
    Advanced chat with DPR using full AI analysis
    """
    dprs_collection = get_dprs_collection()
    
    # Find DPR by ID
    dpr = dprs_collection.find_one({"_id": ObjectId(chat_request.dpr_id)})
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
    from app.models.ai_models import EnhancedDPRExtraction, Recommendation
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
    
    # Answer the question using the chatbot
    answer = ai_service.answer_dpr_question(
        chat_request.question, enhanced_extraction, ai_risk_scores, recommendations
    )
    
    return ChatResponse(
        answer=answer,
        dpr_id=chat_request.dpr_id,
        timestamp=datetime.utcnow()
    )

# Add the translation endpoint with simple translations
@router.post("/translate", response_model=TranslationResponse)
async def translate_text(translation_request: TranslationRequest):
    """
    Translate text to the target language
    """
    try:
        # For English, return original content
        if translation_request.target_lang == 'en':
            return TranslationResponse(
                translated_text=translation_request.text,
                source_lang='en',
                target_lang='en'
            )
        
        # Simple dictionary-based translation for common terms
        # Using ASCII representations to avoid encoding issues
        translations = {
            'Project Title': {
                'hi': 'Project Title (Hindi)',
                'as': 'Project Title (Assamese)'
            },
            'Budget Details': {
                'hi': 'Budget Details (Hindi)',
                'as': 'Budget Details (Assamese)'
            },
            'Timeline': {
                'hi': 'Timeline (Hindi)',
                'as': 'Timeline (Assamese)'
            },
            'Resources & Manpower': {
                'hi': 'Resources & Manpower (Hindi)',
                'as': 'Resources & Manpower (Assamese)'
            },
            'Location / Region': {
                'hi': 'Location / Region (Hindi)',
                'as': 'Location / Region (Assamese)'
            },
            'Environmental Concerns': {
                'hi': 'Environmental Concerns (Hindi)',
                'as': 'Environmental Concerns (Assamese)'
            }
        }
        
        # Check if we have a translation for this text and language
        translated_text = translation_request.text
        if translation_request.text in translations and translation_request.target_lang in translations[translation_request.text]:
            translated_text = translations[translation_request.text][translation_request.target_lang]
        
        return TranslationResponse(
            translated_text=translated_text,
            source_lang='en',
            target_lang=translation_request.target_lang
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )
