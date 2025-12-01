import sys
import os
import pdfplumber

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.nlp_extractor import NLPExtractor

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def main():
    # Extract text from the uploaded PDF
    pdf_path = "Model_DPR_Final 2.0.pdf"
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters from PDF")
    
    # Initialize NLP extractor
    print("Initializing NLP extractor...")
    extractor = NLPExtractor()
    
    # Extract entities
    print("Extracting entities using spaCy and custom patterns...")
    extraction = extractor.extract_entities(text)
    
    # Print results
    print("\n=== EXTRACTED ENTITIES ===")
    print(f"Project Title: {extraction.project_title}")
    print(f"Department: {extraction.department}")
    print(f"Region: {extraction.region}")
    print(f"State: {extraction.state}")
    print(f"District: {extraction.district}")
    print(f"Duration: {extraction.duration}")
    print(f"Estimated Cost: {extraction.estimated_cost}")
    print(f"Fund Allocation: {extraction.fund_allocation}")
    print(f"Contingency: {extraction.contingency}")
    print(f"Start Date: {extraction.start_date}")
    print(f"End Date: {extraction.end_date}")
    print(f"Risk Zone: {extraction.risk_zone}")
    print(f"Number of Employees: {extraction.num_employees}")
    print(f"Location: {extraction.location}")
    print(f"Budget: {extraction.budget}")
    print(f"Timeline: {extraction.timeline}")
    
    print("\n=== MILESTONES ===")
    for milestone in extraction.milestones or []:
        print(f"  - {milestone}")
        
    print("\n=== MACHINERY ===")
    for machine in extraction.machinery or []:
        print(f"  - {machine}")
        
    print("\n=== MATERIALS ===")
    for material in extraction.materials or []:
        print(f"  - {material}")

if __name__ == "__main__":
    main()