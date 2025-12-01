"""
Simple test to verify current extraction logic
"""
import os
from app.utils.dpr_processor import extract_text_from_pdf, extract_dpr_elements

def test_current_extraction():
    """Test current extraction logic"""
    # Read the test PDF
    with open("test_dpr_document.pdf", "rb") as f:
        file_content = f.read()
    
    # Extract text
    text = extract_text_from_pdf(file_content)
    print("Extracted text:")
    print(repr(text))
    print()
    
    # Extract DPR elements
    extracted = extract_dpr_elements(text)
    print("Extracted elements:")
    print(f"Project Title: {repr(extracted.project_title)}")
    print(f"Budget: {repr(extracted.budget)}")
    print(f"Timeline: {repr(extracted.timeline)}")
    print(f"Resources: {repr(extracted.resource_allocation)}")
    print(f"Location: {repr(extracted.location)}")
    print(f"Environmental: {repr(extracted.environmental_risks)}")

if __name__ == "__main__":
    test_current_extraction()