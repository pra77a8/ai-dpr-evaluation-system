import pdfplumber

with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    lines = text.split('\n')
    for i, line in enumerate(lines[10:20]):
        print(f'{i+10}: {repr(line)}')