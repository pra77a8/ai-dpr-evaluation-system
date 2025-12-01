import os
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.dpr_processor import extract_text_from_pdf, extract_dpr_elements

def main():
    # Path to the uploaded PDF
    pdf_path = "../Model_DPR_Final 2.0.pdf"
    
    print("Testing DPR extraction from PDF...")
    
    # Read PDF file
    with open(pdf_path, 'rb') as f:
        file_content = f.read()
    
    print(f"Read {len(file_content)} bytes from PDF")
    
    # Extract text
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(file_content)
    print(f"Extracted {len(text)} characters")
    
    # Show first 500 characters
    print("\nFirst 500 characters of extracted text:")
    print(text[:500])
    
    # Extract DPR elements
    print("\nExtracting DPR elements...")
    dpr_extraction = extract_dpr_elements(text)
    
    # Print results
    print("\n=== DPR EXTRACTION RESULTS ===")
    print(f"Project Title: {dpr_extraction.project_title}")
    print(f"Budget: {dpr_extraction.budget}")
    print(f"Timeline: {dpr_extraction.timeline}")
    print(f"Resource Allocation: {dpr_extraction.resource_allocation}")
    print(f"Location: {dpr_extraction.location}")
    print(f"Environmental Risks: {dpr_extraction.environmental_risks}")
    print(f"Technical Sections: {dpr_extraction.technical_sections}")

if __name__ == "__main__":
    main()