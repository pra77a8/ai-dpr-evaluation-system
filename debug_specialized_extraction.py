"""
Debug the specialized extraction to understand what's happening
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import re
from app.ai.nlp_extractor import NLPExtractor

# Sample text provided by the user
sample_text = """
local communities and support economic development in the region. BUDGET: Total Project Cost: â‚¹30,00,000 Fund Allocation: â‚¹30,00,000 Source of Funds: Government Grant TIMELINE: Project Duration: 18 months Start Date: January 2025 Completion Date: June 2026 Milestones: - Site Preparation: 2 months - Foundation Work: 4 months - Road Construction: 8 months - Finishing & Landscaping: 3 months - Inspection & Handover: 1 month RESOURCES & MANPOWER: - 75 laborers - 8 engineers - 15 vehicles - 2 surveyors - 1 project managerLOCATION / REGION: Project Area: Village Rampur to Highway NH-44 District: East District State: Sample State Geographical Features: Mixed terrain with some hilly areas ENVIRONMENTAL CONCERNS: - Minimal tree cutting required - Flood-prone area during monsoon season - Soil erosion prevention measures to be implemented - Drainage system design to handle heavy rainfall - Wildlife corridor preservation TECHNICAL SPECIFICATIONS: - Road Length: 12 kilometers - Road Width: 7 meters - Surface Material: Bituminous concrete - Drainage System: Culverts and side drains - Safety Features: Guardrails and signage RISK ASSESSMENT: - Cost Overrun Risk: Medium - Schedule Delay Risk: High (due to monsoon) - Resource Availability: Low - Environmental Compliance: Medium APPROVALS: Prepared by: Civil Engineering Department Approved by: District Collector Date of Approval: December 15, 2024 Prepared by: Civil Engineering Department Date: October 6, 2025Approved by: District Collector Approval Date: December 15, 2024
"""

def debug_extraction():
    """Debug the extraction process"""
    print("=== Debugging Extraction Process ===")
    
    # Look for text before "BUDGET:"
    budget_match = re.search(r'(.*?)\s*BUDGET[:\-]', sample_text, re.DOTALL | re.IGNORECASE)
    if budget_match:
        context = budget_match.group(1).strip()
        print(f"Context before BUDGET: '{context}'")
        print(f"Context length: {len(context)}")
        
        # Split into lines
        lines = context.split('\n')
        print(f"Number of lines: {len(lines)}")
        
        # Show last few lines
        print("\nLast 3 lines:")
        for i, line in enumerate(lines[-3:]):
            print(f"  {i+1}: '{line.strip()}' (length: {len(line.strip())})")
            
        # Check for keywords
        if "road" in context.lower() and "construction" in context.lower():
            print("\n✅ Found 'road' and 'construction' in context")
        if "development" in context.lower():
            print("✅ Found 'development' in context")
            
    else:
        print("❌ No BUDGET pattern found")
    
    # Try a different approach - look for the actual project title
    print("\n=== Trying Different Approach ===")
    
    # Since there's no clear project title, let's create one based on content
    if "road" in sample_text.lower() and "construction" in sample_text.lower():
        project_title = "Road Construction and Community Development Project"
    elif "development" in sample_text.lower():
        project_title = "Community Development Project"
    else:
        project_title = "Infrastructure Development Project"
        
    print(f"Generated project title: '{project_title}'")
    
    # Test with the generic extractor
    print("\n=== Testing Generic Extractor ===")
    extractor = NLPExtractor()
    extraction = extractor.extract_entities(sample_text)
    print(f"Generic extractor project title: '{extraction.project_title}'")
    print(f"Generic extractor department: '{extraction.department}'")
    print(f"Generic extractor state: '{extraction.state}'")
    print(f"Generic extractor district: '{extraction.district}'")
    
    # Test our logic
    print("\n=== Testing Our Logic ===")
    if extraction.project_title and len(extraction.project_title) > 200:
        print("✅ Needs special handling (title too long)")
        # Apply our special title
        print(f"✅ Replacing with: '{project_title}'")
    else:
        print("❌ Doesn't need special handling based on length")

if __name__ == "__main__":
    debug_extraction()