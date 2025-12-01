import pdfplumber

# Read the PDF file
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    print(f'Number of pages: {len(pdf.pages)}')
    
    # Print first few pages content
    for i in range(min(3, len(pdf.pages))):
        print(f'\n--- Page {i+1} ---')
        text = pdf.pages[i].extract_text()
        print(text[:1000])  # First 1000 characters