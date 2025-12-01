import pdfplumber

with pdfplumber.open('sample_dpr.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    print(text[:2000])