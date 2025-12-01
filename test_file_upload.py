import requests
import os

def test_file_upload():
    """
    Test file upload to see if there are any issues
    """
    print("Testing file upload...")
    
    # List available PDF files
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found in current directory")
        return
    
    print(f"Found PDF files: {pdf_files}")
    
    # Try to upload the first available PDF file
    test_file = pdf_files[0]
    print(f"Testing upload with: {test_file}")
    
    try:
        with open(test_file, "rb") as f:
            files = {"file": (test_file, f, "application/pdf")}
            data = {"uploaded_by": "test_user"}
            
            print("Sending upload request...")
            response = requests.post(
                "http://127.0.0.1:8005/api/dpr/upload",
                files=files,
                data=data,
                timeout=120  # Increase timeout to 2 minutes
            )
            
            print(f"Upload response: {response.status_code}")
            if response.status_code == 200:
                print("Upload successful!")
                result = response.json()
                print(f"Response keys: {result.keys()}")
                if 'extracted_data' in result:
                    print(f"Extracted project title: {result['extracted_data'].get('project_title', 'N/A')}")
                print(f"Total response size: {len(str(result))} characters")
            else:
                print(f"Upload failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"Upload test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_file_upload()