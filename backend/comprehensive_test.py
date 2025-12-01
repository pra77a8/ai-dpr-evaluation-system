import pdfplumber
from app.ai.nlp_extractor import NLPExtractor

def main():
    # Extract text from the uploaded PDF
    pdf_path = "../Model_DPR_Final 2.0.pdf"
    print("Extracting text from PDF...")
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    
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
        
    print("\n=== VENDOR DETAILS ===")
    for vendor in extraction.vendor_details or []:
        print(f"  - {vendor}")

if __name__ == "__main__":
    main()