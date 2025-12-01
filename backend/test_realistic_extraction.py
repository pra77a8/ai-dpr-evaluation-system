"""
Test script to verify DPR extraction with realistic document format
"""
import os
import sys
from app.utils.dpr_processor import extract_dpr_elements

def test_realistic_dpr_extraction():
    """Test DPR extraction with realistic document format"""
    # Read the realistic DPR text
    sample_file_path = os.path.join(os.path.dirname(__file__), "..", "test_realistic_dpr.txt")
    
    with open(sample_file_path, "r", encoding="utf-8") as f:
        sample_text = f.read()
    
    print("Realistic DPR Text (First 500 chars):")
    print("=" * 50)
    print(sample_text[:500] + "...")
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
    
    # Manual verification
    print("\nManual Verification:")
    print("=" * 50)
    print("Expected values based on document content:")
    print("- Project Title: Rural Road Development - Phase 2")
    print("- Budget: ₹25,00,000")
    print("- Timeline: 12 months")
    print("- Resource Allocation: 50 laborers, 5 engineers, 10 vehicles")
    print("- Location: Village Rampur to Highway NH-44, District East")
    print("- Environmental Risks: Minimal tree cutting required, flood-prone area during monsoon")
    print("=" * 50)

if __name__ == "__main__":
    test_realistic_dpr_extraction()