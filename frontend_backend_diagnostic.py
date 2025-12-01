"""
Comprehensive diagnostic tool for frontend-backend communication issues
"""
import requests
import json
import os
import sys
from pathlib import Path

def check_backend_connectivity():
    """Check if frontend can connect to backend"""
    print("🔍 Checking backend connectivity...")
    
    # Test direct backend access
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is accessible directly")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend on port 8001")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

def check_cors_configuration():
    """Check CORS configuration"""
    print("\n🔍 Checking CORS configuration...")
    
    # This would normally be checked in the frontend, but we can simulate
    print("ℹ️  CORS should allow http://localhost:5173 (Vite dev server)")
    print("ℹ️  Backend CORS is configured in backend/main.py")
    
    # Check if we can make a preflight request
    try:
        response = requests.options("http://localhost:8001/api/dpr/upload", 
                                  headers={"Origin": "http://localhost:5173"},
                                  timeout=5)
        if response.status_code in [200, 204]:
            print("✅ CORS preflight request successful")
        else:
            print(f"⚠️  CORS preflight returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  CORS preflight error: {e}")

def test_file_upload_directly():
    """Test file upload directly to backend"""
    print("\n🔍 Testing direct file upload to backend...")
    
    # Create a test file
    test_content = """Project Title: Rural Road Development - Phase 2
Budget Details: ₹30,00,000 (Thirty Lakhs)
Timeline: 18 months (Jan 2025 - Jun 2026)
Resources & Manpower: 75 laborers, 8 engineers, 15 vehicles
Location / Region: Village Rampur to Highway NH-44, District East
Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon"""
    
    with open("test_upload.txt", "w") as f:
        f.write(test_content)
    
    try:
        with open("test_upload.txt", "rb") as f:
            files = {"file": ("test_upload.txt", f, "text/plain")}
            data = {"uploaded_by": "diagnostic_test"}
            
            response = requests.post("http://localhost:8001/api/dpr/upload", 
                                   files=files, data=data, timeout=30)
            
            if response.status_code == 200:
                print("✅ Direct upload to backend successful")
                result = response.json()
                print("📄 Extracted data:")
                for key, value in result.get("extracted_data", {}).items():
                    print(f"  {key}: {value}")
            else:
                print(f"❌ Direct upload failed with status {response.status_code}")
                print(f"📄 Error: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Direct upload error: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists("test_upload.txt"):
            os.remove("test_upload.txt")
    
    return True

def check_frontend_configuration():
    """Check frontend configuration"""
    print("\n🔍 Checking frontend configuration...")
    
    # Check for vite.config.ts
    vite_config_path = "vite.config.ts"
    if os.path.exists(vite_config_path):
        print("✅ vite.config.ts found")
        # Check for proxy configuration
        with open(vite_config_path, "r") as f:
            content = f.read()
            if "proxy" in content:
                print("✅ Proxy configuration found in vite.config.ts")
            else:
                print("⚠️  No proxy configuration found in vite.config.ts")
                print("   This may cause CORS issues in development")
    else:
        print("❌ vite.config.ts not found")

def check_vite_config():
    """Check Vite proxy configuration"""
    print("\n🔍 Checking Vite proxy configuration...")
    
    vite_config_path = "vite.config.ts"
    if os.path.exists(vite_config_path):
        with open(vite_config_path, "r") as f:
            content = f.read()
            print("📄 vite.config.ts content:")
            print(content[:500] + "..." if len(content) > 500 else content)
            
            # Check for proxy settings
            if "http://localhost:8001" in content:
                print("✅ Proxy to backend (http://localhost:8001) configured")
            else:
                print("⚠️  Proxy to backend not found")
                print("   Add proxy configuration to fix CORS issues")

def create_detailed_frontend_test():
    """Create a detailed frontend test"""
    print("\n🔍 Creating detailed frontend test...")
    
    test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Frontend-Backend Test</title>
</head>
<body>
    <h1>Frontend-Backend Communication Test</h1>
    <input type="file" id="fileInput" accept=".pdf,.txt,.docx">
    <button onclick="testUpload()">Test Upload</button>
    <div id="result"></div>

    <script>
        async function testUpload() {
            const fileInput = document.getElementById('fileInput');
            const resultDiv = document.getElementById('result');
            
            if (!fileInput.files[0]) {
                resultDiv.innerHTML = '<p style="color: red;">Please select a file first</p>';
                return;
            }
            
            const file = fileInput.files[0];
            const formData = new FormData();
            formData.append('file', file);
            formData.append('uploaded_by', 'frontend_test');
            
            resultDiv.innerHTML = '<p>Testing upload...</p>';
            
            try {
                // Try direct backend call
                const response = await fetch('http://localhost:8001/api/dpr/upload', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const result = await response.json();
                    resultDiv.innerHTML = '<p style="color: green;">Direct backend call successful!</p>';
                    resultDiv.innerHTML += '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
                } else {
                    const error = await response.text();
                    resultDiv.innerHTML = '<p style="color: red;">Direct backend call failed: ' + error + '</p>';
                }
            } catch (error) {
                resultDiv.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
                console.error('Upload error:', error);
            }
        }
    </script>
</body>
</html>
    """
    
    with open("frontend_test.html", "w") as f:
        f.write(test_html)
    
    print("✅ Created frontend_test.html")
    print("   Open this file in your browser to test frontend-backend communication")

def check_network_connectivity():
    """Check network connectivity between frontend and backend"""
    print("\n🔍 Checking network connectivity...")
    
    # Check if both ports are listening
    import subprocess
    
    try:
        # Check port 8001 (backend)
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
        if "8001" in result.stdout:
            print("✅ Port 8001 (backend) is listening")
        else:
            print("❌ Port 8001 (backend) is not listening")
            
        # Check port 5173 (frontend)
        if "5173" in result.stdout:
            print("✅ Port 5173 (frontend) is listening")
        else:
            print("⚠️  Port 5173 (frontend) may not be listening")
            
    except Exception as e:
        print(f"⚠️  Cannot check network connectivity: {e}")

def main():
    """Main diagnostic function"""
    print("🔧 Frontend-Backend Communication Diagnostic Tool")
    print("=" * 50)
    
    # Run all checks
    checks = [
        check_backend_connectivity,
        check_cors_configuration,
        test_file_upload_directly,
        check_frontend_configuration,
        check_vite_config,
        check_network_connectivity,
        create_detailed_frontend_test
    ]
    
    for check in checks:
        try:
            check()
        except Exception as e:
            print(f"❌ Error in {check.__name__}: {e}")
    
    print("\n📝 Diagnostic complete!")
    print("\n🔧 Recommendations:")
    print("1. If direct backend calls work but frontend fails, check proxy configuration")
    print("2. If backend is not accessible, ensure it's running on port 8001")
    print("3. Check browser console for detailed error messages")
    print("4. Test with frontend_test.html to isolate the issue")

if __name__ == "__main__":
    main()