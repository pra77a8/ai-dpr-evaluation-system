import requests
import os

def test_upload():
    """Test file upload to see what error occurs"""
    
    # Server URL
    backend_url = "http://localhost:8003"  # Changed to port 8003
    
    # Test PDF file
    pdf_file = "sample_dpr.pdf"
    file_path = os.path.join(os.path.dirname(__file__), pdf_file)
    
    print("=== UPLOAD DEBUG TEST ===")
    print(f"Backend URL: {backend_url}")
    print(f"Testing file: {pdf_file}")
    print()
    
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return
    
    print(f"✓ File found: {file_path}")
    print(f"File size: {os.path.getsize(file_path)} bytes")
    print()
    
    try:
        # Upload PDF file
        with open(file_path, 'rb') as f:
            files = {'file': (pdf_file, f, 'application/pdf')}
            data = {'uploaded_by': 'test_user', 'generate_reports': 'true'}
            
            print("Uploading file...")
            response = requests.post(
                f"{backend_url}/api/dpr/upload_with_ai",
                files=files,
                data=data,
                timeout=30
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✓ Upload successful!")
            result = response.json()
            print(f"Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            if isinstance(result, dict) and "dpr" in result:
                dpr_info = result["dpr"]
                print(f"DPR ID: {dpr_info.get('id', 'Not found')}")
                print(f"File name: {dpr_info.get('file_name', 'Not found')}")
        else:
            print(f"✗ Upload failed")
            print(f"Response Text: {response.text}")
            try:
                error_json = response.json()
                print(f"Error JSON: {error_json}")
            except:
                print("Response is not JSON")
                
    except Exception as e:
        print(f"✗ Error during upload: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_upload()