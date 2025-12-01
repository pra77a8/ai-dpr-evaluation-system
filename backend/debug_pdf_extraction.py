"""
Debug script to see what text is extracted from PDF files
"""
import os
import re
from app.utils.dpr_processor import extract_text_from_pdf, extract_dpr_elements

def debug_pdf_extraction(pdf_file_path):
    """Debug PDF text extraction"""
    if not os.path.exists(pdf_file_path):
        print(f"File not found: {pdf_file_path}")
        return
    
    print(f"Debugging PDF extraction for: {pdf_file_path}")
    print("=" * 50)
    
    # Read the file
    with open(pdf_file_path, 'rb') as f:
        file_content = f.read()
    
    print(f"File size: {len(file_content)} bytes")
    
    # Extract text
    try:
        text = extract_text_from_pdf(file_content)
        print("\nExtracted text:")
        print("-" * 30)
        print(repr(text))  # Show all text
        print("-" * 30)
        
        # Show first few lines
        lines = text.split('\n')
        print("\nLines:")
        for i, line in enumerate(lines[:10]):
            print(f"{i+1:2d}: {repr(line)}")
        
        # Test specific regex patterns
        print("\nTesting regex patterns:")
        print("-" * 30)
        
        # Test project title patterns
        patterns = [
            r'Project Title:\s*([^\n]+)',
            r'Project Title: (Rural Road Development - Phase 2)',
            r'(Rural Road Development - Phase 2)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            print(f"Pattern: {pattern}")
            if match:
                print(f"  Match: {repr(match.group(0))}")
                if match.groups():
                    print(f"  Groups: {match.groups()}")
            else:
                print("  No match")
            print()
        
        # Extract DPR elements
        print("\nDPR Element Extraction:")
        print("-" * 30)
        extracted = extract_dpr_elements(text)
        
        print(f"Project Title: {repr(extracted.project_title)}")
        print(f"Budget: {repr(extracted.budget)}")
        print(f"Timeline: {repr(extracted.timeline)}")
        print(f"Resources: {repr(extracted.resource_allocation)}")
        print(f"Location: {repr(extracted.location)}")
        print(f"Environmental: {repr(extracted.environmental_risks)}")
        
    except Exception as e:
        print(f"Error extracting text: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with our generated PDF
    debug_pdf_extraction("test_dpr_document.pdf")