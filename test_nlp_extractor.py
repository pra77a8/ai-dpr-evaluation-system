"""
Test script for the enhanced NLP extractor with the three specific DPR templates
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import pdfplumber
from app.ai.nlp_extractor import NLPExtractor

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def test_nlp_extractor():
    """Test the enhanced NLP extractor with the three DPR templates"""
    print("=== Testing Enhanced NLP Extractor ===")
    
    # Initialize the extractor
    extractor = NLPExtractor()
    
    # Test files
    templates = [
        ("sample_dpr.pdf", "Sample DPR Template"),
        ("Model_DPR_Final 2.0.pdf", "Model DPR Final 2.0"),
        ("BridgesDPRTemplate[1].pdf", "Bridges DPR Template")
    ]
    
    for pdf_file, pdf_name in templates:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if os.path.exists(pdf_path):
            print(f"\n--- {pdf_name} ---")
            text = extract_text_from_pdf(pdf_path)
            
            if text:
                # Extract entities using the enhanced extractor
                extraction = extractor.extract_entities(text)
                
                # Display key extracted information
                print(f"Project Title: {extraction.project_title}")
                print(f"Department: {extraction.department}")
                print(f"Estimated Cost: {extraction.estimated_cost}")
                print(f"Duration: {extraction.duration}")
                print(f"State: {extraction.state}")
                print(f"District: {extraction.district}")
                print(f"Risk Zone: {extraction.risk_zone}")
            else:
                print("  Failed to extract text from PDF")
        else:
            print(f"  File not found: {pdf_path}")

if __name__ == "__main__":
    test_nlp_extractor()