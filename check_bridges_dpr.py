import pdfplumber

with pdfplumber.open('BridgesDPRTemplate[1].pdf') as pdf:
    print(f"Number of pages: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages):
        if i < 3:  # Check first 3 pages
            print(f"\n--- Page {i+1} ---")
            text = page.extract_text()
            lines = text.split('\n')
            for j, line in enumerate(lines[:10]):
                print(f'{j}: {repr(line)}')