"""
Test the current extractor with the sample text provided by the user
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.nlp_extractor import NLPExtractor

# Sample text provided by the user
sample_text = """
local communities and support economic development in the region. BUDGET: Total Project Cost: â‚¹30,00,000 Fund Allocation: â‚¹30,00,000 Source of Funds: Government Grant TIMELINE: Project Duration: 18 months Start Date: January 2025 Completion Date: June 2026 Milestones: - Site Preparation: 2 months - Foundation Work: 4 months - Road Construction: 8 months - Finishing & Landscaping: 3 months - Inspection & Handover: 1 month RESOURCES & MANPOWER: - 75 laborers - 8 engineers - 15 vehicles - 2 surveyors - 1 project managerLOCATION / REGION: Project Area: Village Rampur to Highway NH-44 District: East District State: Sample State Geographical Features: Mixed terrain with some hilly areas ENVIRONMENTAL CONCERNS: - Minimal tree cutting required - Flood-prone area during monsoon season - Soil erosion prevention measures to be implemented - Drainage system design to handle heavy rainfall - Wildlife corridor preservation TECHNICAL SPECIFICATIONS: - Road Length: 12 kilometers - Road Width: 7 meters - Surface Material: Bituminous concrete - Drainage System: Culverts and side drains - Safety Features: Guardrails and signage RISK ASSESSMENT: - Cost Overrun Risk: Medium - Schedule Delay Risk: High (due to monsoon) - Resource Availability: Low - Environmental Compliance: Medium APPROVALS: Prepared by: Civil Engineering Department Approved by: District Collector Date of Approval: December 15, 2024 Prepared by: Civil Engineering Department Date: October 6, 2025Approved by: District Collector Approval Date: December 15, 2024
"""

def test_sample_text():
    """Test the current extractor with the sample text"""
    print("=== Testing Current Extractor with Sample Text ===")
    
    try:
        # Initialize the extractor
        extractor = NLPExtractor()
        
        # Extract entities
        extraction = extractor.extract_entities(sample_text)
        
        # Print results
        print("\n=== Extraction Results ===")
        print(f"Project Title: {extraction.project_title}")
        print(f"Department: {extraction.department}")
        print(f"Estimated Cost: {extraction.estimated_cost}")
        print(f"Duration: {extraction.duration}")
        print(f"Start Date: {extraction.start_date}")
        print(f"End Date: {extraction.end_date}")
        print(f"State: {extraction.state}")
        print(f"District: {extraction.district}")
        print(f"Risk Zone: {extraction.risk_zone}")
        print(f"Number of Employees: {extraction.num_employees}")
        print(f"Milestones: {extraction.milestones}")
        
        print("\n=== Analysis ===")
        if extraction.project_title:
            print("✅ Project title extracted")
        else:
            print("❌ Project title NOT extracted")
            
        if extraction.estimated_cost:
            print("✅ Estimated cost extracted")
        else:
            print("❌ Estimated cost NOT extracted")
            
        if extraction.duration:
            print("✅ Duration extracted")
        else:
            print("❌ Duration NOT extracted")
            
        if extraction.state:
            print("✅ State extracted")
        else:
            print("❌ State NOT extracted")
            
        return extraction
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    extraction = test_sample_text()