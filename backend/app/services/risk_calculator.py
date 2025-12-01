import random
from app.models.dpr import DPRExtraction
from app.models.risk import RiskScore

def calculate_risk_scores(extracted_data: DPRExtraction) -> RiskScore:
    """
    Calculate risk scores based on extracted DPR data.
    In a real implementation, this would use ML models like XGBoost.
    For this prototype, we'll use rule-based logic with some randomness.
    """
    
    # Initialize risk scores
    cost_overruns = 0.0
    schedule_delays = 0.0
    resource_shortages = 0.0
    environmental_risks = 0.0
    
    # Cost Overruns Risk (0-100)
    if extracted_data.budget:
        # If budget is mentioned but seems low, higher risk
        budget_text = extracted_data.budget.lower()
        if "lakh" in budget_text or "thousand" in budget_text:
            cost_overruns = min(100.0, 30.0 + random.uniform(10, 30))
        elif "crore" in budget_text or "million" in budget_text:
            cost_overruns = min(100.0, 20.0 + random.uniform(5, 20))
        else:
            cost_overruns = min(100.0, 40.0 + random.uniform(10, 30))
    else:
        # No budget mentioned - high risk
        cost_overruns = 70.0 + random.uniform(10, 30)
    
    # Schedule Delays Risk (0-100)
    if extracted_data.timeline:
        # If timeline is mentioned, lower risk
        schedule_delays = 20.0 + random.uniform(5, 25)
    else:
        # No timeline mentioned - high risk
        schedule_delays = 60.0 + random.uniform(20, 40)
    
    # Resource Shortages Risk (0-100)
    if extracted_data.resource_allocation:
        # If resource allocation is mentioned, lower risk
        resource_shortages = 25.0 + random.uniform(10, 30)
    else:
        # No resource allocation mentioned - high risk
        resource_shortages = 65.0 + random.uniform(15, 35)
    
    # Environmental Risks (0-100)
    if extracted_data.environmental_risks:
        # If environmental risks are mentioned, moderate to high risk
        environmental_risks = 40.0 + random.uniform(20, 40)
    else:
        # No environmental risks mentioned - lower risk
        environmental_risks = 15.0 + random.uniform(5, 20)
    
    # Additional logic for incomplete DPRs
    # Count how many key fields are missing
    missing_fields = 0
    if not extracted_data.project_title:
        missing_fields += 1
    if not extracted_data.budget:
        missing_fields += 1
    if not extracted_data.timeline:
        missing_fields += 1
    if not extracted_data.resource_allocation:
        missing_fields += 1
    if not extracted_data.location:
        missing_fields += 1
    if not extracted_data.environmental_risks:
        missing_fields += 1
    
    # Increase overall risk if many fields are missing
    if missing_fields >= 4:
        # Significantly incomplete DPR - very high risk
        cost_overruns = min(100.0, cost_overruns + 20.0)
        schedule_delays = min(100.0, schedule_delays + 25.0)
        resource_shortages = min(100.0, resource_shortages + 25.0)
        environmental_risks = min(100.0, environmental_risks + 15.0)
    elif missing_fields >= 2:
        # Moderately incomplete DPR - increased risk
        cost_overruns = min(100.0, cost_overruns + 10.0)
        schedule_delays = min(100.0, schedule_delays + 15.0)
        resource_shortages = min(100.0, resource_shortages + 15.0)
        environmental_risks = min(100.0, environmental_risks + 10.0)
    
    # Ensure scores are within 0-100 range
    cost_overruns = max(0.0, min(100.0, cost_overruns))
    schedule_delays = max(0.0, min(100.0, schedule_delays))
    resource_shortages = max(0.0, min(100.0, resource_shortages))
    environmental_risks = max(0.0, min(100.0, environmental_risks))
    
    return RiskScore(
        cost_overruns=cost_overruns,
        schedule_delays=schedule_delays,
        resource_shortages=resource_shortages,
        environmental_risks=environmental_risks
    )