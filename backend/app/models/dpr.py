from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List

class FileType(str, Enum):
    PDF = "pdf"
    WORD = "word"
    IMAGE = "image"

class DPRExtraction(BaseModel):
    project_title: Optional[str] = None
    budget: Optional[str] = None
    timeline: Optional[str] = None
    resource_allocation: Optional[str] = None
    location: Optional[str] = None
    environmental_risks: Optional[str] = None
    technical_sections: Optional[List[str]] = None

class DPRReports(BaseModel):
    analytical_report: Optional[str] = None
    recommendation_report: Optional[str] = None

class RiskScores(BaseModel):
    cost_overruns: Optional[float] = None
    schedule_delays: Optional[float] = None
    resource_shortages: Optional[float] = None
    environmental_risks: Optional[float] = None

class DPRBase(BaseModel):
    file_name: str
    file_type: FileType
    uploaded_by: str  # User ID
    extracted_data: DPRExtraction
    reports: Optional[DPRReports] = None

class DPRCreate(BaseModel):
    file_name: str
    file_type: FileType
    uploaded_by: str

class DPRInDB(DPRBase):
    id: str
    uploaded_at: datetime

class DPRResponse(DPRBase):
    id: str
    uploaded_at: datetime
    ai_risk_scores: Optional[RiskScores] = None
    completeness_score: Optional[float] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from database