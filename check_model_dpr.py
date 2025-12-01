"""
Check the Model DPR file content
"""

import pdfplumber

with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    lines = text.split('\n')
    for i, line in enumerate(lines[:15]):
        print(f'{i}: {repr(line)}')

if __name__ == "__main__":
    check_model_dpr()