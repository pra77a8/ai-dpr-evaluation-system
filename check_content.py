import pdfplumber

# Check Model DPR content
print("=== Model DPR Content ===")
text = ""
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    for i, page in enumerate(pdf.pages[:3]):
        text += page.extract_text() or ""
        print(f"Page {i+1}: {repr(page.extract_text()[:200])}")

print("\n=== Bridges DPR Content ===")
text = ""
with pdfplumber.open('BridgesDPRTemplate[1].pdf') as pdf:
    for i, page in enumerate(pdf.pages[:3]):
        text += page.extract_text() or ""
        print(f"Page {i+1}: {repr(page.extract_text()[:200])}")