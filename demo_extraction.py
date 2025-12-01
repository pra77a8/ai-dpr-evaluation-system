"""
Demo script to show how the enhanced DPR extraction works with the uploaded PDF
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import pdfplumber
from backend.app.ai.nlp_extractor import NLPExtractor

def demo_extraction():
    print("=== DPR EXTRACTOR DEMO ===")
    print("Demonstrating enhanced extraction from 'Model_DPR_Final 2.0.pdf'")
    print()
    
    # Extract text from PDF
    pdf_path = "Model_DPR_Final 2.0.pdf"
    print(f"Reading PDF: {pdf_path}")
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        # Just read first 3 pages for demo
        for i in range(min(3, len(pdf.pages))):
            text += pdf.pages[i].extract_text() or ""
    
    print(f"Extracted {len(text)} characters")
    print()
    
    # Initialize extractor
    print("Initializing NLP extractor with spaCy...")
    extractor = NLPExtractor()
    print()
    
    # Extract entities
    print("Extracting entities...")
    extraction = extractor.extract_entities(text)
    print()
    
    # Display key results
    print("=== EXTRACTION RESULTS ===")
    print(f"Project Title: {extraction.project_title}")
    print(f"Department: {extraction.department}")
    print(f"Estimated Cost: {extraction.estimated_cost}")
    print(f"Location: {extraction.location}")
    print(f"State: {extraction.state}")
    print(f"District: {extraction.district}")
    print(f"Timeline: {extraction.timeline}")
    print(f"Risk Zone: {extraction.risk_zone}")
    print()
    
    # Show sample of extracted text
    print("=== SAMPLE EXTRACTED TEXT ===")
    lines = text.split('\n')
    for i, line in enumerate(lines[:15]):
        if line.strip():
            print(f"{i+1:2}: {line[:100]}{'...' if len(line) > 100 else ''}")

if __name__ == "__main__":
    demo_extraction()