"""
Quick test for project title extraction from actual PDF
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
        # Just extract first few pages for testing
        for i, page in enumerate(pdf.pages):
            if i < 3:  # Only first 3 pages
                text += page.extract_text() or ""
    return text

def quick_title_test():
    """Quick test for project title extraction"""
    print("=== Quick Project Title Extraction Test ===")
    
    try:
        # Extract text from PDF (first few pages only)
        text = extract_text_from_pdf("Model_DPR_Final 2.0.pdf")
        print(f"Extracted text length: {len(text)} characters")
        
        # Show first part of the text for debugging
        lines = text.split('\n')
        print("\n=== First 15 lines of PDF ===")
        for i, line in enumerate(lines[:15]):
            print(f"{i+1:2d}: {line[:100]}{'...' if len(line) > 100 else ''}")
        
        # Initialize the generic NLP extractor
        extractor = NLPExtractor()
        
        # Extract entities using the generic approach
        extraction = extractor.extract_entities(text)
        
        # Print project title result
        print(f"\nProject Title: {extraction.project_title}")
            
        # Check if we successfully extracted the project title
        if extraction.project_title and "Roll-Out of National e-Vidhan Application" in extraction.project_title:
            print("\n✅ SUCCESS: Project title correctly extracted!")
            return True
        else:
            print("\n❌ FAILURE: Project title not correctly extracted")
            return False
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_title_test()
    if success:
        print("\n🎉 Generic extraction is working correctly!")
    else:
        print("\n💥 Generic extraction failed.")