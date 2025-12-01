"""
Debug script to see the actual content of the PDF and how it's being processed
"""

import pdfplumber

def debug_pdf_content():
    """Debug the PDF content to understand the structure"""
    pdf_path = "Model_DPR_Final 2.0.pdf"
    
    print("=== PDF Content Debug ===")
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Number of pages: {len(pdf.pages)}")
        
        # Print first few pages content
        for i in range(min(5, len(pdf.pages))):
            print(f"\n--- Page {i+1} ---")
            text = pdf.pages[i].extract_text()
            lines = text.split('\n')
            
            # Print first 20 lines
            for j, line in enumerate(lines[:20]):
                print(f"{j+1:2d}: {line}")
                
            # Look for specific patterns
            print("\nLooking for specific patterns:")
            if "DETAILED PROJECT REPORT" in text:
                print("  Found: DETAILED PROJECT REPORT")
                
            if "For" in text:
                print("  Found: 'For' in text")
                
            if "National e-Vidhan" in text:
                print("  Found: National e-Vidhan")
                
            # Show lines around DPR pattern
            for j, line in enumerate(lines):
                if "DETAILED PROJECT REPORT" in line:
                    print(f"  Line {j+1}: {line}")
                    if j+1 < len(lines):
                        print(f"  Line {j+2}: {lines[j+1]}")
                    if j+2 < len(lines):
                        print(f"  Line {j+3}: {lines[j+2]}")
                    if j+3 < len(lines):
                        print(f"  Line {j+4}: {lines[j+3]}")
                    break

if __name__ == "__main__":
    debug_pdf_content()