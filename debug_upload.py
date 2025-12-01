"""
Debug script to test DPR upload functionality
"""
import requests
import json
import os

def test_dpr_upload():
    """Test uploading a DPR document to the API"""
    url = "http://localhost:8001/api/dpr/upload"
    
    # Check if our test file exists
    test_file_path = "test_dpr_document.txt"
    if not os.path.exists(test_file_path):
        print(f"Test file {test_file_path} not found!")
        print("Creating a sample test file...")
        with open(test_file_path, "w") as f:
            f.write("""Project Title: Rural Road Development - Phase 2

Budget Details: ₹30,00,000 (Thirty Lakhs)

Timeline: 18 months (Jan 2025 - Jun 2026)

Resources & Manpower: 75 laborers, 8 engineers, 15 vehicles

Location / Region: Village Rampur to Highway NH-44, District East

Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon""")
        print(f"Created {test_file_path}")

    print(f"Testing upload to: {url}")
    print(f"Using file: {test_file_path}")
    
    try:
        # Check if backend is accessible
        health_check = requests.get("http://localhost:8001/health", timeout=5)
        print(f"Backend health check: {health_check.status_code}")
        if health_check.status_code == 200:
            print("Backend is running!")
        else:
            print("Backend might not be running properly!")
            return
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend. Make sure it's running on http://localhost:8001")
        return
    except Exception as e:
        print(f"ERROR checking backend: {e}")
        return

    # Try to upload the file
    try:
        with open(test_file_path, "rb") as f:
            files = {"file": (test_file_path, f, "text/plain")}
            data = {"uploaded_by": "debug_user"}
            
            print("Sending upload request...")
            response = requests.post(url, files=files, data=data, timeout=30)
            
            print(f"Upload Status Code: {response.status_code}")
            print(f"Upload Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("SUCCESS: File uploaded successfully!")
                try:
                    result = response.json()
                    print("Response Data:")
                    print(json.dumps(result, indent=2))
                except:
                    print("Response Text:")
                    print(response.text)
            else:
                print(f"ERROR: Upload failed with status code {response.status_code}")
                try:
                    error_result = response.json()
                    print(f"Error Details: {error_result}")
                except:
                    print("Response Text:")
                    print(response.text)
                    # Print first 500 characters of response for debugging
                    print(f"Response preview: {response.text[:500]}")
                    
    except FileNotFoundError:
        print(f"ERROR: File {test_file_path} not found!")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend server. Make sure it's running.")
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out. The server might be busy or not responding.")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

def check_backend_endpoints():
    """Check what endpoints are available on the backend"""
    try:
        # Check main page
        response = requests.get("http://localhost:8001/", timeout=5)
        print(f"Main page: {response.status_code}")
        
        # Check docs
        response = requests.get("http://localhost:8001/docs", timeout=5)
        print(f"Docs page: {response.status_code}")
        
        # Check health
        response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Health data: {response.json()}")
            
    except Exception as e:
        print(f"Error checking endpoints: {e}")

def test_with_proper_file():
    """Test with a proper file type"""
    url = "http://localhost:8001/api/dpr/upload"
    
    print("Testing with proper form data...")
    
    try:
        # Create a simple text file
        test_content = """Project Title: Rural Road Development - Phase 2
Budget Details: ₹30,00,000 (Thirty Lakhs)
Timeline: 18 months (Jan 2025 - Jun 2026)
Resources & Manpower: 75 laborers, 8 engineers, 15 vehicles
Location / Region: Village Rampur to Highway NH-44, District East
Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon"""
        
        # Send as form data
        data = {
            "uploaded_by": "debug_user"
        }
        
        files = {
            "file": ("test.txt", test_content, "text/plain")
        }
        
        print("Sending upload request with proper form data...")
        response = requests.post(url, files=files, data=data, timeout=30)
        
        print(f"Upload Status Code: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS: File uploaded successfully!")
            try:
                result = response.json()
                print("Response Data:")
                print(json.dumps(result, indent=2))
            except:
                print("Response Text:")
                print(response.text)
        else:
            print(f"ERROR: Upload failed with status code {response.status_code}")
            try:
                error_result = response.json()
                print(f"Error Details: {error_result}")
            except:
                print("Response Text:")
                print(response.text)
                
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== DPR Upload Debug Tool ===")
    print()
    
    print("1. Checking backend endpoints...")
    check_backend_endpoints()
    print()
    
    print("2. Testing DPR upload with file object...")
    test_dpr_upload()
    print()
    
    print("3. Testing DPR upload with proper form data...")
    test_with_proper_file()