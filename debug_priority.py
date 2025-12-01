import pdfplumber
import sys
import os
import re

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.nlp_extractor import NLPExtractor

# Extract text from Model DPR (first few pages)
text = ""
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        if i < 3:  # Check first 3 pages
            text += page.extract_text() or ""

print("=== Full Debug of NLP Extractor ===")

# Let's manually step through the _extract_project_title_enhanced method
lines = text.split('\n')

print("\n1. Testing Sample DPR Pattern (Project: [Title]):")
project_pattern = r'Project:\s*([^\n]+)'
match = re.search(project_pattern, text, re.IGNORECASE)
if match:
    title = match.group(1).strip()
    print(f"   Match: {repr(title)}")
else:
    print("   No match")

print("\n2. Testing Model DPR Special Pattern (For ...):")
for i, line in enumerate(lines):
    if line.strip().lower() == "for" and i + 1 < len(lines):
        print(f"   Found 'For' at line {i}: {repr(line)}")
        print(f"   Next line {i+1}: {repr(lines[i+1])}")
        print(f"   Line {i+2}: {repr(lines[i+2])}")
        # Collect the next few lines as the project title
        title_lines = []
        j = i + 1
        # Collect lines until we hit a line that looks like it's not part of the title
        while j < len(lines) and lines[j].strip() and not any(keyword in lines[j].lower() for keyword in ['in', 'project', 'tentative', 'outlay']):
            title_lines.append(lines[j].strip())
            print(f"     Adding line {j}: {repr(lines[j])}")
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
            if title and len(title) > 3:
                print(f"   *** This should be the final result ***")
        break

print("\n3. Let's see what the actual extractor returns:")
extractor = NLPExtractor()
result = extractor._extract_project_title_enhanced(text, {})
print(f"   Extractor result: {repr(result)}")