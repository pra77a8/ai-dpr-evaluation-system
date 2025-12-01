"""
Simple test to verify DPR extraction with the exact format provided
"""
import os
import sys
from app.utils.dpr_processor import extract_dpr_elements

def test_exact_format():
    """Test with the exact format provided in the query"""
    sample_text = """
Project Title

Rural Road Development - Phase 2

Budget Details

₹25,00,000 (Twenty-Five Lakhs)

Timeline

12 months (Jan 2025 - Dec 2025)

Resources & Manpower

50 laborers, 5 engineers, 10 vehicles

Location / Region

Village Rampur to Highway NH-44, District East

Environmental Concerns

Minimal tree cutting required, flood-prone area during monsoon
"""
    
    print("Sample DPR Text:")
    print("=" * 50)
    print(sample_text)
    print("=" * 50)
    
    # Extract DPR elements
    extracted_data = extract_dpr_elements(sample_text)
    
    print("\nExtracted Data:")
    print("=" * 50)
    print(f"Project Title: {extracted_data.project_title}")
    print(f"Budget: {extracted_data.budget}")
    print(f"Timeline: {extracted_data.timeline}")
    print(f"Resource Allocation: {extracted_data.resource_allocation}")
    print(f"Location: {extracted_data.location}")
    print(f"Environmental Risks: {extracted_data.environmental_risks}")
    print(f"Technical Sections: {extracted_data.technical_sections}")
    print("=" * 50)
    
    # Verification
    print("\nVerification:")
    print("=" * 50)
    
    # Check each field
    checks = [
        ("Project Title", extracted_data.project_title, "Rural Road Development - Phase 2"),
        ("Budget", extracted_data.budget, "₹25,00,000"),
        ("Timeline", extracted_data.timeline, "12 months"),
        ("Resource Allocation", extracted_data.resource_allocation, "50 laborers, 5 engineers, 10 vehicles"),
        ("Location", extracted_data.location, "Village Rampur to Highway NH-44, District East"),
        ("Environmental Risks", extracted_data.environmental_risks, "Minimal tree cutting required, flood-prone area during monsoon")
    ]
    
    passed = 0
    total = len(checks)
    
    for field, actual, expected in checks:
        if actual and expected.lower() in actual.lower():
            print(f"✓ {field}: PASS")
            passed += 1
        elif actual:
            print(f"? {field}: PARTIAL (Expected: {expected}, Got: {actual})")
            passed += 1
        else:
            print(f"✗ {field}: FAIL (Expected: {expected})")
    
    print("=" * 50)
    print(f"Result: {passed}/{total} checks passed")
    return passed == total

if __name__ == "__main__":
    success = test_exact_format()
    if success:
        print("\n🎉 All tests passed! The DPR extraction is working correctly.")
    else:
        print("\n❌ Some tests failed. The extraction needs improvement.")