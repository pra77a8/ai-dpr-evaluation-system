"""
Test script for just the Model DPR template
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

def test_model_dpr():
    """Test the Model DPR template"""
    pdf_path = os.path.join(os.path.dirname(__file__), "Model_DPR_Final 2.0.pdf")
    if os.path.exists(pdf_path):
        print("=== Model DPR Final 2.0 ===")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Initialize the extractor
            extractor = NLPExtractor()
            
            # Extract entities using the enhanced extractor
            extraction = extractor.extract_entities(text)
            
            # Display key extracted information
            print(f"Project Title: {repr(extraction.project_title)}")
            print(f"Department: {repr(extraction.department)}")
            print(f"Estimated Cost: {repr(extraction.estimated_cost)}")
            print(f"Duration: {repr(extraction.duration)}")
            print(f"State: {repr(extraction.state)}")
            print(f"District: {repr(extraction.district)}")
            print(f"Risk Zone: {repr(extraction.risk_zone)}")
        else:
            print("  Failed to extract text from PDF")
    else:
        print(f"  File not found: {pdf_path}")

if __name__ == "__main__":
    test_model_dpr()