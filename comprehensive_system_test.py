"""
Comprehensive test to verify the entire system is working correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService
from app.utils.dpr_processor import extract_text_from_pdf
from app.models.dpr import DPRExtraction

# Sample text with the problematic format
sample_text = """
local communities and support economic development in the region. BUDGET: Total Project Cost: ₹30,00,000 Fund Allocation: ₹30,00,000 Source of Funds: Government Grant TIMELINE: Project Duration: 18 months Start Date: January 2025 Completion Date: June 2026 Milestones: - Site Preparation: 2 months - Foundation Work: 4 months - Road Construction: 8 months - Finishing & Landscaping: 3 months - Inspection & Handover: 1 month RESOURCES & MANPOWER: - 75 laborers - 8 engineers - 15 vehicles - 2 surveyors - 1 project managerLOCATION / REGION: Project Area: Village Rampur to Highway NH-44 District: East District State: Sample State Geographical Features: Mixed terrain with some hilly areas ENVIRONMENTAL CONCERNS: - Minimal tree cutting required - Flood-prone area during monsoon season - Soil erosion prevention measures to be implemented - Drainage system design to handle heavy rainfall - Wildlife corridor preservation TECHNICAL SPECIFICATIONS: - Road Length: 12 kilometers - Road Width: 7 meters - Surface Material: Bituminous concrete - Drainage System: Culverts and side drains - Safety Features: Guardrails and signage RISK ASSESSMENT: - Cost Overrun Risk: Medium - Schedule Delay Risk: High (due to monsoon) - Resource Availability: Low - Environmental Compliance: Medium APPROVALS: Prepared by: Civil Engineering Department Approved by: District Collector Date of Approval: December 15, 2024 Prepared by: Civil Engineering Department Date: October 6, 2025Approved by: District Collector Approval Date: December 15, 2024
"""

def test_comprehensive_system():
    """Test the entire system with the problematic format"""
    print("=== Comprehensive System Test ===")
    
    # Test 1: AI Service with specialized extraction
    print("\n1. Testing AI Service with Specialized Extraction...")
    ai_service = AIService()
    enhanced_extraction = ai_service.extract_dpr_entities(sample_text)
    
    print(f"   Project Title: {enhanced_extraction.project_title}")
    print(f"   Department: {enhanced_extraction.department}")
    print(f"   State: {enhanced_extraction.state}")
    print(f"   District: {enhanced_extraction.district}")
    
    # Verify the results
    assert enhanced_extraction.project_title == "Road Construction and Community Development Project", f"Expected 'Road Construction and Community Development Project', got '{enhanced_extraction.project_title}'"
    assert enhanced_extraction.department == "Civil Engineering Department", f"Expected 'Civil Engineering Department', got '{enhanced_extraction.department}'"
    assert enhanced_extraction.state == "Sample State", f"Expected 'Sample State', got '{enhanced_extraction.state}'"
    assert enhanced_extraction.district == "East District", f"Expected 'East District', got '{enhanced_extraction.district}'"
    
    print("   ✅ AI Service test passed")
    
    # Test 2: DPR Extraction compatibility
    print("\n2. Testing DPR Extraction Compatibility...")
    dpr_extraction = DPRExtraction(
        project_title=enhanced_extraction.project_title,
        budget=enhanced_extraction.budget,
        timeline=enhanced_extraction.timeline,
        resource_allocation=enhanced_extraction.resource_allocation,
        location=enhanced_extraction.location,
        environmental_risks=enhanced_extraction.environmental_risks,
        technical_sections=enhanced_extraction.technical_sections
    )
    
    print(f"   DPR Project Title: {dpr_extraction.project_title}")
    print(f"   DPR Location: {dpr_extraction.location}")
    
    assert dpr_extraction.project_title == "Road Construction and Community Development Project", f"Expected 'Road Construction and Community Development Project', got '{dpr_extraction.project_title}'"
    
    print("   ✅ DPR Extraction compatibility test passed")
    
    # Test 3: Risk Analysis
    print("\n3. Testing Risk Analysis...")
    risk_scores = ai_service.predict_dpr_risks(enhanced_extraction)
    print(f"   Risk scores calculated: {len(risk_scores)} risks")
    
    assert isinstance(risk_scores, dict), "Risk scores should be a dictionary"
    assert len(risk_scores) > 0, "Should have at least one risk score"
    
    print("   ✅ Risk Analysis test passed")
    
    # Test 4: Recommendations
    print("\n4. Testing Recommendations...")
    recommendations = ai_service.generate_recommendations(risk_scores)
    print(f"   Recommendations generated: {len(recommendations)}")
    
    assert isinstance(recommendations, list), "Recommendations should be a list"
    
    print("   ✅ Recommendations test passed")
    
    print("\n=== All Tests Passed ===")
    print("The system is now correctly handling the problematic format!")
    print("\nKey improvements:")
    print("- Specialized extractor generates meaningful project titles")
    print("- State and district information is correctly extracted")
    print("- Department information is properly identified")
    print("- Full AI analysis pipeline works correctly")
    print("- Backward compatibility maintained")

if __name__ == "__main__":
    test_comprehensive_system()