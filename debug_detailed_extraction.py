"""
Detailed debug test to see what's happening with the extraction
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService
from app.ai.specialized_dpr_extractor import SpecializedDPRExtractor
from app.ai.nlp_extractor import NLPExtractor

# The problematic sample text
sample_text = """
local communities and support economic development in the region. BUDGET: Total Project Cost: ₹30,00,000 Fund Allocation: ₹30,00,000 Source of Funds: Government Grant TIMELINE: Project Duration: 18 months Start Date: January 2025 Completion Date: June 2026 Milestones: - Site Preparation: 2 months - Foundation Work: 4 months - Road Construction: 8 months - Finishing & Landscaping: 3 months - Inspection & Handover: 1 month RESOURCES & MANPOWER: - 75 laborers - 8 engineers - 15 vehicles - 2 surveyors - 1 project managerLOCATION / REGION: Project Area: Village Rampur to Highway NH-44 District: East District State: Sample State Geographical Features: Mixed terrain with some hilly areas ENVIRONMENTAL CONCERNS: - Minimal tree cutting required - Flood-prone area during monsoon season - Soil erosion prevention measures to be implemented - Drainage system design to handle heavy rainfall - Wildlife corridor preservation TECHNICAL SPECIFICATIONS: - Road Length: 12 kilometers - Road Width: 7 meters - Surface Material: Bituminous concrete - Drainage System: Culverts and side drains - Safety Features: Guardrails and signage RISK ASSESSMENT: - Cost Overrun Risk: Medium - Schedule Delay Risk: High (due to monsoon) - Resource Availability: Low - Environmental Compliance: Medium APPROVALS: Prepared by: Civil Engineering Department Approved by: District Collector Date of Approval: December 15, 2024 Prepared by: Civil Engineering Department Date: October 6, 2025Approved by: District Collector Approval Date: December 15, 2024
"""

def debug_extraction():
    """Debug the extraction process in detail"""
    print("=== Detailed Extraction Debug ===")
    
    # Test 1: Generic extractor
    print("\n1. Testing Generic Extractor:")
    generic_extractor = NLPExtractor()
    generic_result = generic_extractor.extract_entities(sample_text)
    print(f"   Generic Project Title: '{generic_result.project_title}'")
    print(f"   Generic Title Length: {len(generic_result.project_title) if generic_result.project_title else 0}")
    
    # Test 2: Specialized extractor
    print("\n2. Testing Specialized Extractor:")
    specialized_extractor = SpecializedDPRExtractor()
    specialized_result = specialized_extractor.extract_entities(sample_text)
    print(f"   Specialized Project Title: '{specialized_result.project_title}'")
    print(f"   Specialized Title Length: {len(specialized_result.project_title) if specialized_result.project_title else 0}")
    
    # Test 3: AI Service
    print("\n3. Testing AI Service:")
    ai_service = AIService()
    ai_result = ai_service.extract_dpr_entities(sample_text)
    print(f"   AI Service Project Title: '{ai_result.project_title}'")
    print(f"   AI Service Title Length: {len(ai_result.project_title) if ai_result.project_title else 0}")
    
    # Analyze the text before BUDGET
    import re
    budget_match = re.search(r'(.*?)\s*BUDGET[:\-]', sample_text, re.DOTALL | re.IGNORECASE)
    if budget_match:
        context = budget_match.group(1).strip()
        print(f"\n4. Text before BUDGET:")
        print(f"   Context: '{context}'")
        print(f"   Context Length: {len(context)}")
        
        # Check for keywords
        if "local communities" in context.lower():
            print("   ✅ Contains 'local communities'")
        if "development" in context.lower():
            print("   ✅ Contains 'development'")
        if "road" in sample_text.lower():
            print("   ✅ Contains 'road'")
        if "construction" in sample_text.lower():
            print("   ✅ Contains 'construction'")
    
    print("\n=== Analysis ===")
    if ai_result.project_title == "Road Construction and Community Development Project":
        print("✅ SUCCESS: AI Service is generating the correct title!")
    elif len(ai_result.project_title) > 200:
        print("❌ ISSUE: AI Service is still returning the long text")
        print(f"   Returned: '{ai_result.project_title[:100]}...'")
    else:
        print(f"? UNCLEAR: AI Service returned: '{ai_result.project_title}'")

if __name__ == "__main__":
    debug_extraction()