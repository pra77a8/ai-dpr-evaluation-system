import pdfplumber

with pdfplumber.open('sample_dpr.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    lines = text.split('\n')
    for i, line in enumerate(lines[:10]):
        print(f'{i}: {repr(line)}')