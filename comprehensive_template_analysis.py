"""
Comprehensive analysis of all DPR templates to improve extraction patterns
"""

import pdfplumber
import os
import re

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file (first few pages)"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract first 3 pages for analysis
            for i, page in enumerate(pdf.pages):
                if i < 3:
                    text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def analyze_templates():
    """Analyze all DPR templates and create improved patterns"""
    print("=== Comprehensive DPR Template Analysis ===")
    
    templates = [
        ("sample_dpr.pdf", "Sample DPR Template"),
        ("Model_DPR_Final 2.0.pdf", "Model DPR Final 2.0"),
        ("BridgesDPRTemplate[1].pdf", "Bridges DPR Template")
    ]
    
    all_patterns = {
        'project_title': [],
        'cost': [],
        'timeline': [],
        'department': []
    }
    
    for pdf_file, pdf_name in templates:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if os.path.exists(pdf_path):
            print(f"\n--- {pdf_name} ---")
            text = extract_text_from_pdf(pdf_path)
            
            if text:
                # Analyze project title patterns
                lines = text.split('\n')
                
                # Look for common project title patterns
                for i, line in enumerate(lines[:30]):  # Check first 30 lines
                    # Pattern 1: "Project: [Title]"
                    if line.strip().startswith("Project:"):
                        title = line.split("Project:", 1)[1].strip()
                        if title:
                            print(f"  Project Title Pattern 1: '{title}'")
                            all_patterns['project_title'].append(f"Project:\\s*([^\n]+)")
                    
                    # Pattern 2: "Project Title: [Title]"
                    if line.strip().startswith("Project Title:"):
                        title = line.split("Project Title:", 1)[1].strip()
                        if title:
                            print(f"  Project Title Pattern 2: '{title}'")
                            all_patterns['project_title'].append(f"Project Title:\\s*([^\n]+)")
                    
                    # Pattern 3: "DETAILED PROJECT REPORT (DPR) For [Title]"
                    if "DETAILED PROJECT REPORT" in line and "For" in line:
                        print(f"  Project Title Pattern 3: Line contains DPR and For")
                        all_patterns['project_title'].append(f"DETAILED PROJECT REPORT.*?For\\s*([^\n]+)")
                    
                    # Pattern 4: Line after "For" (as seen in Model DPR)
                    if line.strip() == "For" and i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not next_line.startswith(("Project:", "Project Title:", "DETAILED")):
                            print(f"  Project Title Pattern 4: Line after 'For' -> '{next_line}'")
                            # This is a contextual pattern, we'll handle it in code
                
                # Look for cost patterns
                cost_matches = re.findall(r'[₹Rs.]+\s*[\d,]+', text)
                if cost_matches:
                    print(f"  Cost Patterns Found: {len(cost_matches[:3])} examples")
                    for match in cost_matches[:3]:
                        print(f"    '{match}'")
                    all_patterns['cost'].append(r'[₹Rs.]+\s*[\d,]+')
                
                # Look for specific cost section patterns
                cost_section_matches = re.findall(r'(?:Total Project Cost|Fund Allocation|Budget):\s*[₹Rs.]*\s*[\d,]+', text, re.IGNORECASE)
                if cost_section_matches:
                    print(f"  Cost Section Patterns Found: {len(cost_section_matches[:3])} examples")
                    for match in cost_section_matches[:3]:
                        print(f"    '{match}'")
                    all_patterns['cost'].append(r'(?:Total Project Cost|Fund Allocation|Budget):\s*[₹Rs.]*\s*[\d,]+')
                
                # Look for timeline patterns
                timeline_matches = re.findall(r'(?:Project Duration|Duration|Timeline):\s*\d+\s*(?:months?|years?)', text, re.IGNORECASE)
                if timeline_matches:
                    print(f"  Timeline Patterns Found: {len(timeline_matches[:3])} examples")
                    for match in timeline_matches[:3]:
                        print(f"    '{match}'")
                    all_patterns['timeline'].append(r'(?:Project Duration|Duration|Timeline):\s*\d+\s*(?:months?|years?)')
                
                # Look for department patterns
                dept_matches = re.findall(r'(?:Prepared by|Department):\s*([^\n]+)', text, re.IGNORECASE)
                if dept_matches:
                    print(f"  Department Patterns Found: {len(dept_matches[:3])} examples")
                    for match in dept_matches[:3]:
                        print(f"    '{match}'")
                    all_patterns['department'].append(r'(?:Prepared by|Department):\s*([^\n]+)')
    
    # Create improved patterns
    print(f"\n=== Improved Extraction Patterns ===")
    create_improved_patterns(all_patterns)

def create_improved_patterns(patterns):
    """Create improved regex patterns based on analysis"""
    
    # Improved project title patterns
    project_title_patterns = [
        # Standard DPR format
        r'DETAILED PROJECT REPORT.*?For\s*([^\n]+)',
        # Project title format
        r'Project Title[:\-]?\s*([^\n]+)',
        # Project format
        r'Project[:\-]?\s*([^\n]+)',
        # Contextual pattern for "For" followed by title
        # This will be handled in code logic
    ]
    
    # Improved cost patterns
    cost_patterns = [
        r'(?:Total Project Cost|Fund Allocation|Budget|Estimated Cost|Outlay)[:\-]?\s*[₹Rs.]*\s*([\d,]+(?:\.\d+)?)',
        r'[₹Rs.]+\s*([\d,]+(?:\.\d+)?)',
        r'([\d,]+(?:\.\d+)?)\s*(?:crore|lakh|million|billion)'
    ]
    
    # Improved timeline patterns
    timeline_patterns = [
        r'(?:Project Duration|Duration|Timeline)[:\-]?\s*(\d+\s*(?:months?|years?))',
        r'(\d+\s*(?:months?|years?))'
    ]
    
    # Improved department patterns
    department_patterns = [
        r'(?:Prepared by|Department|Ministry)[:\-]?\s*([^\n]+)',
        r'(Civil Engineering Department|Public Works Department|Road Construction Department)'
    ]
    
    print("Project Title Patterns:")
    for pattern in project_title_patterns:
        print(f"  {pattern}")
    
    print("\nCost Patterns:")
    for pattern in cost_patterns:
        print(f"  {pattern}")
    
    print("\nTimeline Patterns:")
    for pattern in timeline_patterns:
        print(f"  {pattern}")
    
    print("\nDepartment Patterns:")
    for pattern in department_patterns:
        print(f"  {pattern}")
    
    # Update the NLP extractor with these improved patterns
    update_nlp_extractor(project_title_patterns, cost_patterns, timeline_patterns, department_patterns)

def update_nlp_extractor(project_patterns, cost_patterns, timeline_patterns, dept_patterns):
    """Update the NLP extractor with improved patterns"""
    print(f"\n=== Updating NLP Extractor ===")
    print("The following improvements will be made to the NLP extractor:")
    print("1. Enhanced project title extraction with multiple strategies")
    print("2. Better cost pattern matching for Indian currency formats")
    print("3. Improved timeline detection for months/years")
    print("4. More robust department identification")
    print("5. Contextual extraction for 'For' pattern (line after 'For')")
    
    # This would be implemented in the actual code
    print("\nImplementation plan:")
    print("- Update patterns in backend/app/ai/nlp_extractor.py")
    print("- Improve _extract_project_title_generic method")
    print("- Enhance _extract_custom_entities method")
    print("- Add better contextual analysis for special formats")

if __name__ == "__main__":
    analyze_templates()