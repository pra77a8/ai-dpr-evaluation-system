import requests
import json

# Test the organization dashboard endpoint
response = requests.get("http://localhost:8005/api/dpr/organization/dashboard")

if response.status_code == 200:
    data = response.json()
    print("Response status: 200 OK")
    print("Number of DPRs returned:", len(data))
    
    # Print the first DPR to see its structure
    if data:
        first_dpr = data[0]
        print("\nFirst DPR structure:")
        print(json.dumps(first_dpr, indent=2))
        
        # Check if ai_risk_scores and completeness_score are present
        print("\nChecking for required fields:")
        print("ai_risk_scores present:", "ai_risk_scores" in first_dpr)
        print("completeness_score present:", "completeness_score" in first_dpr)
        
        if "ai_risk_scores" in first_dpr:
            print("ai_risk_scores value:", first_dpr["ai_risk_scores"])
        if "completeness_score" in first_dpr:
            print("completeness_score value:", first_dpr["completeness_score"])
else:
    print(f"Error: {response.status_code}")
    print(response.text)