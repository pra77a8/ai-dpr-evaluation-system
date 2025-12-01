import pdfplumber
import re

# Extract text from sample DPR
with pdfplumber.open('sample_dpr.pdf') as pdf:
    text = pdf.pages[0].extract_text()

# Print the text around "Total Project Cost" to see the actual format
if 'Total Project Cost' in text:
    start_idx = text.find('Total Project Cost')
    end_idx = start_idx + 100
    print("Text around 'Total Project Cost':")
    print(repr(text[start_idx-50:end_idx]))

# Try different regex patterns with Unicode rupee symbol
patterns = [
    r'Total Project Cost[:\-]?\s*[₹Rsâ‚¹.]*\s*([\d,]+)',
    r'(?:Total Project Cost|Fund Allocation|Budget|Estimated Cost|Outlay)[:\-]?\s*[₹Rsâ‚¹.]*\s*([\d,]+(?:\.\d+)?)',
    r'Total Project Cost[:\-]?\s*[₹Rsâ‚¹.]*\s*([\d,]+(?:\.\d+)?)',
    r'Total Project Cost:\s*([₹Rsâ‚¹.]*\s*[\d,]+)',
    r'Total Project Cost[:\-]?\s*([₹Rsâ‚¹.]*\s*[\d,]+)'
]

for pattern in patterns:
    match = re.search(pattern, text, re.IGNORECASE)
    print(f"\nPattern: {pattern}")
    print(f"Match: {match}")
    if match:
        print(f"Group 1: {match.group(1)}")