import pdfplumber

with pdfplumber.open('BridgesDPRTemplate[1].pdf') as pdf:
    text = ""
    # Extract first 3 pages
    for i in range(min(3, len(pdf.pages))):
        text += pdf.pages[i].extract_text() + "\n"
    print(text[:2000])