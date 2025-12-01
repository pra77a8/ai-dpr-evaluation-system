from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class EnhancedDPRExtraction(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    # Project Info
    project_title: Optional[str] = None
    department: Optional[str] = None
    region: Optional[str] = None
    duration: Optional[str] = None
    
    # Financial Data
    estimated_cost: Optional[str] = None
    fund_allocation: Optional[str] = None
    yearly_budget: Optional[str] = None
    contingency: Optional[str] = None
    
    # Timeline Data
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    milestones: Optional[List[str]] = None
    
    # Resource Data
    num_employees: Optional[int] = None
    machinery: Optional[List[str]] = None
    raw_materials: Optional[List[str]] = None
    vendor_details: Optional[List[str]] = None
    
    # Location & Geography
    state: Optional[str] = None
    district: Optional[str] = None
    coordinates: Optional[str] = None
    risk_zone: Optional[str] = None  # Flood/Landslide/Connectivity
    
    # Technical Sections
    engineering_details: Optional[str] = None
    specifications: Optional[str] = None
    materials: Optional[List[str]] = None
    
    # Compliance
    guidelines_followed: Optional[bool] = None
    missing_documents: Optional[List[str]] = None
    
    # Extracted from existing model
    budget: Optional[str] = None
    timeline: Optional[str] = None
    resource_allocation: Optional[str] = None
    location: Optional[str] = None
    environmental_risks: Optional[str] = None
    technical_sections: Optional[List[str]] = None

class RiskLabel(str, Enum):
    COST_OVERRUN = "Cost Overrun"
    DELAY = "Delay"
    ENVIRONMENTAL = "Environmental"
    RESOURCE = "Resource"
    NONE = "None"

class Recommendation(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    improvement_type: str  # Budget Rebalance, Timeline Adjustment, etc.
    description: str
    priority: str  # High, Medium, Low

class TrainingDataPoint(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    dpr_id: str
    extracted_data: EnhancedDPRExtraction
    risk_label: RiskLabel
    recommendation: Recommendation
    features: Dict[str, Any]  # Numerical features for ML model