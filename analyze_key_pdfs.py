"""
Analyze the key PDF templates to understand their structure
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

def find_project_title_patterns(text):
    """Find project title patterns in the text"""
    lines = text.split('\n')
    
    # Look for common project title patterns
    title_patterns = [
        "Project:",
        "Project Title:",
        "DETAILED PROJECT REPORT",
        "DPR"
    ]
    
    titles = []
    for i, line in enumerate(lines):
        for pattern in title_patterns:
            if pattern in line:
                if pattern == "Project:" or pattern == "Project Title:":
                    title = line.split(pattern, 1)[1].strip()
                    titles.append((pattern, title, i))
                elif pattern == "DETAILED PROJECT REPORT":
                    # Look for the line after this
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith(("Project:", "Project Title:")):
                            titles.append((pattern, next_line, i))
    
    return titles

def find_cost_patterns(text):
    """Find cost patterns in the text"""
    import re
    
    # Look for currency patterns
    cost_patterns = [
        r'[₹Rs.]+\s*[\d,]+',
        r'Total Project Cost:\s*[₹Rs.]*\s*[\d,]+',
        r'Fund Allocation:\s*[₹Rs.]*\s*[\d,]+',
        r'Budget:\s*[₹Rs.]*\s*[\d,]+'
    ]
    
    costs = []
    for pattern in cost_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        costs.extend(matches)
    
    return costs

def find_timeline_patterns(text):
    """Find timeline patterns in the text"""
    import re
    
    # Look for duration patterns
    timeline_patterns = [
        r'Project Duration:\s*\d+\s*(?:months?|years?)',
        r'Duration:\s*\d+\s*(?:months?|years?)',
        r'Timeline:\s*\d+\s*(?:months?|years?)',
        r'\d+\s*(?:months?|years?)'
    ]
    
    timelines = []
    for pattern in timeline_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        timelines.extend(matches)
    
    return timelines

def analyze_pdf(pdf_path, pdf_name):
    """Analyze a specific PDF"""
    print(f"\n=== {pdf_name} Analysis ===")
    
    text = extract_text_from_pdf(pdf_path)
    if not text:
        print("Failed to extract text")
        return
    
    print(f"Text length: {len(text)} characters")
    
    # Find project titles
    titles = find_project_title_patterns(text)
    print(f"\nProject Titles Found: {len(titles)}")
    for pattern, title, line_num in titles:
        print(f"  {pattern} -> '{title}' (line {line_num})")
    
    # Find costs
    costs = find_cost_patterns(text)
    print(f"\nCosts Found: {len(costs)}")
    for cost in costs[:5]:  # Show first 5
        print(f"  '{cost}'")
    
    # Find timelines
    timelines = find_timeline_patterns(text)
    print(f"\nTimelines Found: {len(timelines)}")
    for timeline in timelines[:5]:  # Show first 5
        print(f"  '{timeline}'")
    
    # Show first few lines to understand structure
    lines = text.split('\n')[:20]
    print(f"\nFirst 20 lines:")
    for i, line in enumerate(lines):
        print(f"{i+1:2d}: {line[:100]}{'...' if len(line) > 100 else ''}")

def main():
    """Main function"""
    pdf_files = [
        ("sample_dpr.pdf", "Sample DPR Template"),
        ("Model_DPR_Final 2.0.pdf", "Model DPR Final 2.0")
    ]
    
    for pdf_file, pdf_name in pdf_files:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if os.path.exists(pdf_path):
            analyze_pdf(pdf_path, pdf_name)
        else:
            print(f"\n=== {pdf_name} ===")
            print(f"File not found: {pdf_path}")

if __name__ == "__main__":
    main()