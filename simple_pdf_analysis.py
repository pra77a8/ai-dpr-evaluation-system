"""
Simple analysis of PDF templates
"""

import pdfplumber
import os

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

def analyze_model_dpr():
    """Analyze the Model DPR Final 2.0 PDF"""
    pdf_path = os.path.join(os.path.dirname(__file__), "Model_DPR_Final 2.0.pdf")
    
    print("=== Model DPR Final 2.0 Analysis ===")
    
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Failed to extract text")
        return
    
    print(f"Text length: {len(text)} characters")
    
    # Show first 30 lines to understand structure
    lines = text.split('\n')[:30]
    print(f"\nFirst 30 lines:")
    for i, line in enumerate(lines):
        print(f"{i+1:2d}: {line[:80]}{'...' if len(line) > 80 else ''}")
        
    # Look for project title patterns
    print(f"\nLooking for project title patterns:")
    for i, line in enumerate(lines[:20]):
        if "DETAILED PROJECT REPORT" in line:
            print(f"  Found 'DETAILED PROJECT REPORT' at line {i+1}")
        if "For" in line:
            print(f"  Found 'For' at line {i+1}: {line}")
        if "Project" in line and ":" in line:
            print(f"  Found project pattern at line {i+1}: {line}")

if __name__ == "__main__":
    analyze_model_dpr()