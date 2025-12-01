import pdfplumber
import sys
import os
import re

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Extract text from Model DPR
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    text = pdf.pages[0].extract_text()

print("=== Debugging Model DPR Title Extraction ===")
lines = text.split('\n')
for i, line in enumerate(lines[:20]):
    print(f'{i}: {repr(line)}')

print("\n=== Testing Special Pattern ===")
# Look for "For" followed by the project title on the next lines
for i, line in enumerate(lines):
    if line.strip().lower() == "for" and i + 1 < len(lines):
        print(f'Found "For" at line {i}')
        # Collect the next few lines as the project title
        title_lines = []
        j = i + 1
        # Collect lines until we hit a line that looks like it's not part of the title
        while j < len(lines) and lines[j].strip() and not any(keyword in lines[j].lower() for keyword in ['in', 'project', 'tentative', 'outlay']):
            title_lines.append(lines[j].strip())
            print(f'  Added line {j}: {repr(lines[j].strip())}')
            j += 1
        if title_lines:
            title = ' '.join(title_lines).strip()
            print(f'Collected title lines: {title_lines}')
            print(f'Joined title: {repr(title)}')
            # Remove "Application(NeVA)" if it's at the end
            if title.endswith("Application(NeVA)"):
                title = title[:-17].strip()
                print(f'After removing "Application(NeVA)": {repr(title)}')
            # Remove "Application" if it's at the end
            elif title.endswith("Application"):
                title = title[:-11].strip()
                print(f'After removing "Application": {repr(title)}')
            # Remove "(NeVA)" if it's at the end
            elif title.endswith("(NeVA)"):
                title = title[:-6].strip()
                print(f'After removing "(NeVA)": {repr(title)}')
            print(f'Final title: {repr(title)}')
        else:
            print("No title lines collected")
        break