"""
Test the generic extraction with the actual PDF file
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import pdfplumber
from app.ai.nlp_extractor import NLPExtractor

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def test_with_actual_pdf():
    """Test the generic extraction with the actual PDF"""
    print("=== Testing Generic DPR Extraction with Actual PDF ===")
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf("Model_DPR_Final 2.0.pdf")
        print("Text extracted successfully from PDF")
        print(f"Extracted text length: {len(text)} characters")
        
        # Show first part of the text for debugging
        lines = text.split('\n')
        print("\n=== First 20 lines of PDF ===")
        for i, line in enumerate(lines[:20]):
            print(f"{i+1:2d}: {line}")
        
        # Initialize the generic NLP extractor
        extractor = NLPExtractor()
        
        # Extract entities using the generic approach
        extraction = extractor.extract_entities(text)
        
        # Print results
        print("\n=== Extraction Results ===")
        print(f"Project Title: {extraction.project_title}")
        print(f"Department: {extraction.department}")
        print(f"Estimated Cost: {extraction.estimated_cost}")
        print(f"Duration: {extraction.duration}")
        print(f"Region: {extraction.region}")
        print(f"State: {extraction.state}")
        print(f"District: {extraction.district}")
        print(f"Risk Zone: {extraction.risk_zone}")
        print(f"Number of Employees: {extraction.num_employees}")
        print(f"Milestones: {extraction.milestones}")
        print(f"Machinery: {extraction.machinery}")
        print(f"Materials: {extraction.materials}")
        print(f"Vendor Details: {extraction.vendor_details}")
        print(f"Guidelines Followed: {extraction.guidelines_followed}")
        print(f"Missing Documents: {extraction.missing_documents}")
            
        print("\n=== Test completed ===")
        
        # Check if we successfully extracted the project title
        if extraction.project_title and "Roll-Out of National e-Vidhan Application" in extraction.project_title:
            print("\n✅ SUCCESS: Project title correctly extracted from actual PDF!")
            return True
        else:
            print("\n❌ FAILURE: Project title not correctly extracted from actual PDF")
            return False
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_with_actual_pdf()
    if success:
        print("\n🎉 Generic extraction is working correctly with the actual PDF!")
    else:
        print("\n💥 Generic extraction failed with the actual PDF.")