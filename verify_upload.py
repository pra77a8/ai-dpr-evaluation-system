"""
Simple script to verify DPR upload is working
"""

import requests
import os

def test_health():
    """Test if the server is healthy"""
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print("✅ Server is healthy")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server health check error: {str(e)}")
        return False

def test_upload():
    """Test uploading a DPR document"""
    url = "http://127.0.0.1:8000/api/dpr/upload_with_ai"
    
    # Path to the uploaded PDF
    pdf_path = "Model_DPR_Final 2.0.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found!")
        return False
    
    # Prepare the file and form data
    files = {
        'file': (pdf_path, open(pdf_path, 'rb'), 'application/pdf')
    }
    
    data = {
        'uploaded_by': 'test_user'
    }
    
    try:
        print("📤 Uploading DPR document...")
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            print(f"File Name: {result.get('dpr', {}).get('file_name')}")
            
            # Extracted data
            extracted_data = result.get('dpr', {}).get('extracted_data', {})
            print(f"Project Title: {extracted_data.get('project_title')}")
            print(f"Budget: {extracted_data.get('budget')}")
            
            return True
        else:
            print(f"❌ Upload failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {str(e)}")
        return False
    finally:
        # Close the file
        if 'files' in locals():
            files['file'][1].close()

if __name__ == "__main__":
    print("=== DPR Upload Verification ===")
    
    # Test server health
    if test_health():
        # Test upload
        test_upload()
    else:
        print("❌ Server is not healthy. Cannot proceed with upload test.")