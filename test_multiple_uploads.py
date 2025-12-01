import requests
import os
import time

def test_multiple_uploads():
    """Test uploading multiple PDF files to verify different risk analytics"""
    
    # Server URL
    backend_url = "http://localhost:8003"
    
    # Test PDF files
    pdf_files = [
        ("sample_dpr.pdf", "Sample DPR"),
        ("Model_DPR_Final 2.0.pdf", "Model DPR"),
        ("BridgesDPRTemplate[1].pdf", "Bridges Template")
    ]
    
    print("=== MULTIPLE UPLOAD TEST ===")
    print(f"Backend URL: {backend_url}")
    print()
    
    results = []
    
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
                    timeout=60  # Increased timeout for larger files
                )
            
            if response.status_code == 200:
                result = response.json()
                ai_risk_scores = result.get('ai_risk_scores', {})
                dpr_info = result.get('dpr', {})
                
                print(f"  ✓ Upload successful")
                print(f"  DPR ID: {dpr_info.get('id', 'N/A')}")
                print(f"  Project Title: {dpr_info.get('enhanced_extraction', {}).get('project_title', 'N/A')}")
                print(f"  Risk Scores:")
                for risk_type, score in ai_risk_scores.items():
                    print(f"    {risk_type}: {score:.4f}")
                
                results.append({
                    'file': pdf_file,
                    'description': description,
                    'dpr_id': dpr_info.get('id', 'N/A'),
                    'project_title': dpr_info.get('enhanced_extraction', {}).get('project_title', 'N/A'),
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
    if len(results) >= 2:
        for i in range(len(results)):
            for j in range(i+1, len(results)):
                result1 = results[i]
                result2 = results[j]
                
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
    test_multiple_uploads()