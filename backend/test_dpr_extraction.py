"""
Test script to verify DPR extraction functionality
"""
import os
import sys
from app.utils.dpr_processor import extract_dpr_elements

def test_dpr_extraction():
    """Test DPR extraction with sample data"""
    # Read the sample DPR text
    sample_file_path = os.path.join(os.path.dirname(__file__), "..", "test_sample_dpr.txt")
    
    with open(sample_file_path, "r", encoding="utf-8") as f:
        sample_text = f.read()
    
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
    
    expected_values = {
        "project_title": "Rural Road Development - Phase 2",
        "budget": "₹25,00,000",
        "timeline": "12 months",
        "resource_allocation": "50 laborers, 5 engineers, 10 vehicles",
        "location": "Village Rampur to Highway NH-44, District East",
        "environmental_risks": "Minimal tree cutting required, flood-prone area during monsoon"
    }
    
    matches = 0
    total = len(expected_values)
    
    for key, expected in expected_values.items():
        actual = getattr(extracted_data, key)
        if actual and expected.lower() in actual.lower():
            print(f"✓ {key.replace('_', ' ').title()}: Match")
            matches += 1
        elif actual:
            print(f"? {key.replace('_', ' ').title()}: Partial match")
            print(f"  Expected: {expected}")
            print(f"  Actual: {actual}")
        else:
            print(f"✗ {key.replace('_', ' ').title()}: Not found")
            print(f"  Expected: {expected}")
    
    print("=" * 50)
    print(f"Accuracy: {matches}/{total} ({(matches/total)*100:.1f}%)")

if __name__ == "__main__":
    test_dpr_extraction()