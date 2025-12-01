import requests
import json

# Test the upload with a simple approach
url = "http://localhost:8001/api/dpr/upload"

# Simple test data
test_content = """Project Title: Rural Road Development - Phase 2
Budget Details: ₹30,00,000 (Thirty Lakhs)
Timeline: 18 months (Jan 2025 - Jun 2026)
Resources & Manpower: 75 laborers, 8 engineers, 15 vehicles
Location / Region: Village Rampur to Highway NH-44, District East
Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon"""

print("Testing DPR upload...")
print(f"URL: {url}")

# Send as form data with PDF content type
data = {
    "uploaded_by": "debug_user"
}

files = {
    "file": ("test.pdf", test_content, "application/pdf")
}

try:
    print("Sending request...")
    response = requests.post(url, files=files, data=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS!")
        print("Response:", response.json())
    else:
        print("ERROR!")
        print("Response text:", response.text)
        
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()