"""
Test script to verify project title extraction
"""

import pdfplumber
from backend.app.ai.nlp_extractor import NLPExtractor

def test_project_title_extraction():
    """Test project title extraction from the PDF"""
    pdf_path = "Model_DPR_Final 2.0.pdf"
    
    print("=== Testing Project Title Extraction ===")
    
    # Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
    
    print(f"Extracted {len(text)} characters from PDF")
    
    # Test the NLP extractor
    extractor = NLPExtractor()
    extraction = extractor.extract_entities(text)
    
    print(f"Extracted Project Title: '{extraction.project_title}'")
    
    # Also test with the basic DPR processor
    from backend.app.utils.dpr_processor import extract_dpr_elements
    dpr_extraction = extract_dpr_elements(text)
    print(f"DPR Processor Project Title: '{dpr_extraction.project_title}'")
    
    # Show first few lines for reference
    lines = text.split('\n')
    print("\nFirst 10 lines of PDF:")
    for i, line in enumerate(lines[:10]):
        print(f"{i+1:2d}: {line}")

if __name__ == "__main__":
    test_project_title_extraction()