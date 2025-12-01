from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class RiskScore(BaseModel):
    cost_overruns: float  # 0-100
    schedule_delays: float  # 0-100
    resource_shortages: float  # 0-100
    environmental_risks: float  # 0-100

class RiskBase(BaseModel):
    dpr_id: str
    project_title: str
    calculated_at: datetime
    risk_scores: RiskScore

class RiskCreate(BaseModel):
    dpr_id: str
    project_title: str
    risk_scores: RiskScore

class RiskInDB(RiskBase):
    id: str

class RiskResponse(RiskBase):
    id: str