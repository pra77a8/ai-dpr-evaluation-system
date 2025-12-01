import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.utils.dpr_processor import extract_text_from_pdf

def examine_pdf_text():
    # Test with actual PDF files
    pdf_files = [
        "sample_dpr.pdf",
        "Model_DPR_Final 2.0.pdf",
        "BridgesDPRTemplate[1].pdf"
    ]
    
    print("=== EXAMINING PDF TEXT CONTENT ===\n")
    
    for pdf_file in pdf_files:
        file_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if not os.path.exists(file_path):
            print(f"File not found: {pdf_file}")
            continue
            
        print(f"--- Examining {pdf_file.upper()} ---")
        
        try:
            # Extract text from PDF
            print("\n1. Extracting text from PDF...")
            with open(file_path, "rb") as f:
                pdf_content = f.read()
            text = extract_text_from_pdf(pdf_content)
            print(f"Extracted text length: {len(text)} characters")
            
            # Show first 1000 characters
            print(f"\nFirst 1000 characters:")
            print("="*50)
            print(repr(text[:1000]))
            print("="*50)
            
            # Show last 1000 characters
            print(f"\nLast 1000 characters:")
            print("="*50)
            print(repr(text[-1000:]))
            print("="*50)
            
            # Look for specific patterns
            print(f"\nLooking for specific patterns:")
            
            # Project title patterns
            import re
            project_patterns = [
                r'Project Title[:\-]?\s*([^\n]+)',
                r'Project:\s*([^\n]+)',
                r'DETAILED PROJECT REPORT \(DPR\)\s*\nFor\s*\n([^\n]+)',
                r'DETAILED PROJECT REPORT \(DPR\)\s*\nFor\s+([^\n]+)'
            ]
            
            for pattern in project_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    print(f"  Pattern '{pattern}': {matches}")
            
            # Duration patterns
            duration_patterns = [
                r'Duration[:\-]?\s*(\d+\s*(?:months?|years?))',
                r'(\d+\s*(?:months?|years?))'
            ]
            
            for pattern in duration_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    print(f"  Duration pattern '{pattern}': {matches}")
            
            # Cost patterns
            cost_patterns = [
                r'(?:Total Project Cost|Fund Allocation|Budget|Estimated Cost|Outlay|Project Tentative Outlay)[:\-]?\s*([₹Rsâ‚¹.]*\s*[\d,]+(?:\.\d+)?)',
                r'[₹Rsâ‚¹.]*\s*[\d,]+(?:\.\d+)?\s*(?:crore|lakh|million|billion)'
            ]
            
            for pattern in cost_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    print(f"  Cost pattern '{pattern}': {matches}")
            
            # Employee patterns
            employee_patterns = [
                r'(?:no\.?|number of)\s*(?:employees?|workers?|staff|laborers|engineers|manpower)[:\-]?\s*(\d+)',
                r'(\d+)\s*(?:employees?|workers?|staff|laborers|engineers|manpower)'
            ]
            
            for pattern in employee_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    print(f"  Employee pattern '{pattern}': {matches}")
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    examine_pdf_text()