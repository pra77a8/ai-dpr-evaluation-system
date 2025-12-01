"""
Very simple final test
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService

# The problematic sample text
sample_text = """
local communities and support economic development in the region. BUDGET: Total Project Cost: ₹30,00,000 Fund Allocation: ₹30,00,000 Source of Funds: Government Grant TIMELINE: Project Duration: 18 months Start Date: January 2025 Completion Date: June 2026 Milestones: - Site Preparation: 2 months - Foundation Work: 4 months - Road Construction: 8 months - Finishing & Landscaping: 3 months - Inspection & Handover: 1 month RESOURCES & MANPOWER: - 75 laborers - 8 engineers - 15 vehicles - 2 surveyors - 1 project managerLOCATION / REGION: Project Area: Village Rampur to Highway NH-44 District: East District State: Sample State Geographical Features: Mixed terrain with some hilly areas ENVIRONMENTAL CONCERNS: - Minimal tree cutting required - Flood-prone area during monsoon season - Soil erosion prevention measures to be implemented - Drainage system design to handle heavy rainfall - Wildlife corridor preservation TECHNICAL SPECIFICATIONS: - Road Length: 12 kilometers - Road Width: 7 meters - Surface Material: Bituminous concrete - Drainage System: Culverts and side drains - Safety Features: Guardrails and signage RISK ASSESSMENT: - Cost Overrun Risk: Medium - Schedule Delay Risk: High (due to monsoon) - Resource Availability: Low - Environmental Compliance: Medium APPROVALS: Prepared by: Civil Engineering Department Approved by: District Collector Date of Approval: December 15, 2024 Prepared by: Civil Engineering Department Date: October 6, 2025Approved by: District Collector Approval Date: December 15, 2024
"""

def very_simple_test():
    """Very simple test"""
    print("Testing AI Service...")
    ai_service = AIService()
    result = ai_service.extract_dpr_entities(sample_text)
    print(f"Project Title: '{result.project_title}'")
    
    if result.project_title == "Road Construction and Community Development Project":
        print("SUCCESS!")
    else:
        print("ISSUE!")

if __name__ == "__main__":
    very_simple_test()