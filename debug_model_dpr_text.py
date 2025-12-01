import pdfplumber

# Extract text from Model DPR (first few pages)
text = ""
with pdfplumber.open('Model_DPR_Final 2.0.pdf') as pdf:
    for i, page in enumerate(pdf.pages):
        if i < 3:  # Check first 3 pages
            text += page.extract_text() or ""

print("=== First 1000 characters of text ===")
print(repr(text[:1000]))

print("\n=== Looking for patterns in the full text ===")
# Check if there's a sentence that matches the extracted title
if "This project aims at providing computer facilities and infrastructure" in text:
    print("Found the problematic text in the full text!")
    
    # Find where this text appears
    start_idx = text.find("This project aims at providing computer facilities and infrastructure")
    print(f"Text found at index {start_idx}")
    print(f"Context: {repr(text[start_idx-50:start_idx+100])}")
else:
    print("Did not find the problematic text in the first 3 pages")
    
    # Let's check if there are generic patterns that might match
    lines = text.split('\n')
    for i, line in enumerate(lines[:30]):
        if "This project aims" in line:
            print(f"Found 'This project aims' at line {i}: {repr(line)}")