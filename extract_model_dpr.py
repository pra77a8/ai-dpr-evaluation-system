import pdfplumber

with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    text = pdf.pages[0].extract_text()
    print(text[:1000])