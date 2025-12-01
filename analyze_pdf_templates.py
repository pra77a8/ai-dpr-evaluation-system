"""
Analyze the PDF templates to understand their structure and improve extraction patterns
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

def analyze_pdf_structure(pdf_path, pdf_name):
    """Analyze the structure of a PDF template"""
    print(f"\n=== Analyzing {pdf_name} ===")
    
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Failed to extract text")
        return
    
    print(f"Total characters: {len(text)}")
    
    # Show first 500 characters to understand structure
    print("\nFirst 500 characters:")
    print(text[:500])
    
    # Show last 500 characters
    print("\nLast 500 characters:")
    print(text[-500:] if len(text) > 500 else text)
    
    # Look for common patterns
    patterns_to_check = [
        "Project Title",
        "DETAILED PROJECT REPORT",
        "DPR",
        "Cost",
        "Budget",
        "Amount",
        "Rs.",
        "₹",
        "Duration",
        "Timeline",
        "Department",
        "State",
        "District",
        "Location"
    ]
    
    print("\nPattern Analysis:")
    for pattern in patterns_to_check:
        if pattern.lower() in text.lower():
            # Find all occurrences
            count = text.lower().count(pattern.lower())
            print(f"  '{pattern}': Found {count} occurrence(s)")
            
            # Show context around first occurrence
            index = text.lower().find(pattern.lower())
            if index != -1:
                start = max(0, index - 50)
                end = min(len(text), index + len(pattern) + 50)
                context = text[start:end].replace('\n', ' ')
                print(f"    Context: ...{context}...")

def main():
    """Main function to analyze all PDF templates"""
    pdf_files = [
        ("sample_dpr.pdf", "Sample DPR Template"),
        ("Model_DPR_Final 2.0.pdf", "Model DPR Final 2.0"),
        ("BridgesDPRTemplate[1].pdf", "Bridges DPR Template")
    ]
    
    for pdf_file, pdf_name in pdf_files:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if os.path.exists(pdf_path):
            analyze_pdf_structure(pdf_path, pdf_name)
        else:
            print(f"\n=== {pdf_name} ===")
            print(f"File not found: {pdf_path}")

if __name__ == "__main__":
    main()