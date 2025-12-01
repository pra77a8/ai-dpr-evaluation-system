from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any
from app.services.chatbot import get_dpr_context, generate_response

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    dpr_id: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_dpr(chat_request: ChatRequest):
    # Get DPR context
    dpr_context = get_dpr_context(chat_request.dpr_id)
    
    if not dpr_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Generate response
    answer = generate_response(chat_request.question, dpr_context)
    
    return ChatResponse(answer=answer)

# Additional endpoint for testing chat functionality
@router.post("/chat/test")
async def test_chat(chat_request: ChatRequest):
    """
    Test endpoint to verify chat functionality with sample data
    """
    # Get DPR context
    dpr_context = get_dpr_context(chat_request.dpr_id)
    
    if not dpr_context:
        # Create sample context for testing
        sample_context = {
            "enhanced_extraction": {
                "project_title": "Road Construction and Community Development Project",
                "department": "Civil Engineering Department",
                "estimated_cost": "₹150 crore",
                "duration": "18 months",
                "state": "Assam",
                "district": "Guwahati",
                "risk_zone": "Flood prone area",
                "num_employees": 150,
                "milestones": ["Site Preparation", "Foundation Work", "Construction", "Finishing"],
                "machinery": ["Excavators", "Bulldozers", "Crane"],
                "materials": ["Cement", "Steel", "Sand"],
                "guidelines_followed": True,
                "missing_documents": ["Environmental Clearance Certificate"]
            },
            "risk_scores": {
                "Cost Risk": 0.65,
                "Schedule Risk": 0.45,
                "Resource Risk": 0.30,
                "Environmental Risk": 0.80,
                "Technical Risk": 0.25
            },
            "recommendations": [
                {
                    "improvement_type": "Budget Rebalance",
                    "description": "Increase contingency budget by 10-15%",
                    "priority": "High"
                },
                {
                    "improvement_type": "Risk Mitigation",
                    "description": "Area prone to flood/landslide — require mitigation planning",
                    "priority": "High"
                },
                {
                    "improvement_type": "Timeline Review",
                    "description": "Consider adding buffer time to critical milestones",
                    "priority": "Medium"
                }
            ]
        }
        answer = generate_response(chat_request.question, sample_context)
    else:
        # Generate response with actual DPR context
        answer = generate_response(chat_request.question, dpr_context)
    
    return ChatResponse(answer=answer)