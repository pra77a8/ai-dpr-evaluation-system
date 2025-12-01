"""
Final verification test to confirm that the system produces different risk analytics for different PDFs
"""

import requests
import time
import os

def test_different_risk_analytics():
    """Test that different PDFs produce different risk analytics"""
    
    # Server URLs
    backend_url = "http://localhost:8000"
    frontend_url = "http://localhost:3002"
    
    # Test PDF files
    pdf_files = [
        ("sample_dpr.pdf", "Sample DPR"),
        ("Model_DPR_Final 2.0.pdf", "Model DPR"),
        ("BridgesDPRTemplate[1].pdf", "Bridges Template")
    ]
    
    print("=== FINAL VERIFICATION TEST ===")
    print(f"Backend URL: {backend_url}")
    print(f"Frontend URL: {frontend_url}")
    print()
    
    # Check if servers are running
    try:
        backend_response = requests.get(f"{backend_url}/health", timeout=5)
        print(f"✓ Backend server is running (Status: {backend_response.status_code})")
    except Exception as e:
        print(f"✗ Backend server is not accessible: {e}")
        return
    
    try:
        frontend_response = requests.get(frontend_url, timeout=5)
        print(f"✓ Frontend server is running (Status: {frontend_response.status_code})")
    except Exception as e:
        print(f"✗ Frontend server is not accessible: {e}")
        return
    
    print()
    
    # Test each PDF file
    risk_results = []
    
    for pdf_file, description in pdf_files:
        file_path = os.path.join(os.path.dirname(__file__), pdf_file)
        
        if not os.path.exists(file_path):
            print(f"⚠ Skipping {description} - File not found: {pdf_file}")
            continue
            
        print(f"Testing {description} ({pdf_file})...")
        
        try:
            # Upload PDF file
            with open(file_path, 'rb') as f:
                files = {'file': (pdf_file, f, 'application/pdf')}
                data = {'uploaded_by': 'test_user', 'generate_reports': 'true'}
                
                response = requests.post(
                    f"{backend_url}/api/dpr/upload_with_ai",
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                ai_risk_scores = result.get('ai_risk_scores', {})
                
                print(f"  ✓ Upload successful")
                print(f"  Project Title: {result.get('dpr', {}).get('enhanced_extraction', {}).get('project_title', 'N/A')}")
                print(f"  Risk Scores:")
                for risk_type, score in ai_risk_scores.items():
                    print(f"    {risk_type}: {score:.4f}")
                
                risk_results.append({
                    'file': pdf_file,
                    'description': description,
                    'project_title': result.get('dpr', {}).get('enhanced_extraction', {}).get('project_title', 'N/A'),
                    'risk_scores': ai_risk_scores
                })
                
            else:
                print(f"  ✗ Upload failed (Status: {response.status_code})")
                print(f"  Response: {response.text}")
                
        except Exception as e:
            print(f"  ✗ Error uploading {pdf_file}: {e}")
        
        print()
        time.sleep(2)  # Wait between uploads
    
    # Compare risk scores
    print("=== RISK SCORE COMPARISON ===")
    if len(risk_results) >= 2:
        for i in range(len(risk_results)):
            for j in range(i+1, len(risk_results)):
                result1 = risk_results[i]
                result2 = risk_results[j]
                
                print(f"Comparing {result1['description']} vs {result2['description']}:")
                
                # Check if any risk scores are different
                has_differences = False
                for risk_type in result1['risk_scores'].keys():
                    score1 = result1['risk_scores'].get(risk_type, 0)
                    score2 = result2['risk_scores'].get(risk_type, 0)
                    
                    if abs(score1 - score2) > 0.01:  # More than 1% difference
                        print(f"  {risk_type}: {score1:.4f} vs {score2:.4f} (DIFFERENT)")
                        has_differences = True
                    else:
                        print(f"  {risk_type}: {score1:.4f} vs {score2:.4f} (similar)")
                
                if has_differences:
                    print(f"  ✓ {result1['description']} and {result2['description']} produce different risk analytics")
                else:
                    print(f"  ⚠ {result1['description']} and {result2['description']} produce similar risk analytics")
                
                print()
    else:
        print("Not enough successful uploads to compare risk scores")
    
    print("=== TEST COMPLETE ===")

if __name__ == "__main__":
    test_different_risk_analytics()