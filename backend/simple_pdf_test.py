import pdfplumber

# Simple test to see PDF content
with pdfplumber.open("../Model_DPR_Final 2.0.pdf") as pdf:
    print(f"Number of pages: {len(pdf.pages)}")
    
    # Print first page content
    print("\nFirst page content:")
    text = pdf.pages[0].extract_text()
    print(text)
    
    # Look for project title pattern
    if "DETAILED PROJECT REPORT (DPR)" in text:
        print("\nFound DPR header!")
        
    # Look for project name pattern
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "For" in line:
            print(f"\nLine with 'For': {line}")
            if i+1 < len(lines):
                print(f"Next line: {lines[i+1]}")