import pdfplumber
import sys
import os
import re

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.nlp_extractor import NLPExtractor

# Extract text from Model DPR
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    text = pdf.pages[0].extract_text()

print("=== Full Text Preview ===")
lines = text.split('\n')
for i, line in enumerate(lines[:20]):
    print(f'{i}: {repr(line)}')

print("\n=== Testing NLP Extractor Step by Step ===")
extractor = NLPExtractor()

# Test each pattern individually
print("\n1. Testing Sample DPR Pattern (Project: [Title]):")
project_pattern = r'Project:\s*([^\n]+)'
match = re.search(project_pattern, text, re.IGNORECASE)
if match:
    title = match.group(1).strip()
    print(f"   Match: {repr(title)}")
else:
    print("   No match")

print("\n2. Testing Model DPR Special Pattern (For ...):")
# Look for "For" followed by the project title on the next lines
for i, line in enumerate(lines):
    if line.strip().lower() == "for" and i + 1 < len(lines):
        print(f"   Found 'For' at line {i}")
        # Collect the next few lines as the project title
        title_lines = []
        j = i + 1
        # Collect lines until we hit a line that looks like it's not part of the title
        while j < len(lines) and lines[j].strip() and not any(keyword in lines[j].lower() for keyword in ['in', 'project', 'tentative', 'outlay']):
            title_lines.append(lines[j].strip())
            j += 1
        if title_lines:
            title = ' '.join(title_lines).strip()
            print(f"   Collected title lines: {title_lines}")
            print(f"   Joined title: {repr(title)}")
            # Remove "Application(NeVA)" if it's at the end
            if title.endswith("Application(NeVA)"):
                title = title[:-17].strip()
            # Remove "Application" if it's at the end
            elif title.endswith("Application"):
                title = title[:-11].strip()
            # Remove "(NeVA)" if it's at the end
            elif title.endswith("(NeVA)"):
                title = title[:-6].strip()
            print(f"   Final title: {repr(title)}")
        break

print("\n3. Testing Full Extractor:")
extraction = extractor.extract_entities(text)
print(f"   Project Title: {repr(extraction.project_title)}")