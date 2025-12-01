"""
Quick verification that the system is working correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService

# Simple test text
test_text = """
local communities and support economic development in the region. BUDGET: Total Project Cost: ₹30,00,000 Fund Allocation: ₹30,00,000 Source of Funds: Government Grant TIMELINE: Project Duration: 18 months Start Date: January 2025 Completion Date: June 2026 Milestones: - Site Preparation: 2 months - Foundation Work: 4 months - Road Construction: 8 months - Finishing & Landscaping: 3 months - Inspection & Handover: 1 month RESOURCES & MANPOWER: - 75 laborers - 8 engineers - 15 vehicles - 2 surveyors - 1 project managerLOCATION / REGION: Project Area: Village Rampur to Highway NH-44 District: East District State: Sample State Geographical Features: Mixed terrain with some hilly areas ENVIRONMENTAL CONCERNS: - Minimal tree cutting required - Flood-prone area during monsoon season - Soil erosion prevention measures to be implemented - Drainage system design to handle heavy rainfall - Wildlife corridor preservation TECHNICAL SPECIFICATIONS: - Road Length: 12 kilometers - Road Width: 7 meters - Surface Material: Bituminous concrete - Drainage System: Culverts and side drains - Safety Features: Guardrails and signage RISK ASSESSMENT: - Cost Overrun Risk: Medium - Schedule Delay Risk: High (due to monsoon) - Resource Availability: Low - Environmental Compliance: Medium APPROVALS: Prepared by: Civil Engineering Department Approved by: District Collector Date of Approval: December 15, 2024 Prepared by: Civil Engineering Department Date: October 6, 2025Approved by: District Collector Approval Date: December 15, 2024
"""

def quick_test():
    """Quick test to verify the system"""
    print("=== Quick Verification Test ===")
    
    # Initialize AI service
    ai_service = AIService()
    
    # Extract entities
    extraction = ai_service.extract_dpr_entities(test_text)
    
    print(f"Project Title: {extraction.project_title}")
    print(f"Department: {extraction.department}")
    print(f"State: {extraction.state}")
    print(f"District: {extraction.district}")
    print(f"Duration: {extraction.duration}")
    
    # Check if we got the improved results
    if extraction.project_title == "Road Construction and Community Development Project":
        print("\n✅ SUCCESS: Specialized extraction is working correctly!")
        print("   The system now generates meaningful project titles instead of long text.")
    else:
        print(f"\n❌ ISSUE: Project title is still: {extraction.project_title}")
        
    if extraction.department == "Civil Engineering Department":
        print("✅ SUCCESS: Department extraction is working correctly!")
    else:
        print(f"❌ ISSUE: Department is: {extraction.department}")
        
    if extraction.state == "Sample State":
        print("✅ SUCCESS: State extraction is working correctly!")
    else:
        print(f"❌ ISSUE: State is: {extraction.state}")
        
    if extraction.district == "East District":
        print("✅ SUCCESS: District extraction is working correctly!")
    else:
        print(f"❌ ISSUE: District is: {extraction.district}")

if __name__ == "__main__":
    quick_test()