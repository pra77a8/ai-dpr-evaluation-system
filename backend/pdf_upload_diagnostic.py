"""
Comprehensive diagnostic script for PDF upload issues
"""
import requests
import json
import os
import sys
from pathlib import Path

def check_backend_health():
    """Check if backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8001")
        return False
    except Exception as e:
        print(f"❌ Error checking backend health: {e}")
        return False

def check_file_validity(file_path):
    """Check if file exists and is valid"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    if os.path.getsize(file_path) == 0:
        print(f"❌ File is empty: {file_path}")
        return False
    
    print(f"✅ File exists: {file_path}")
    print(f"✅ File size: {os.path.getsize(file_path)} bytes")
    return True

def check_file_type(file_path):
    """Check file type and validity"""
    try:
        # Check file extension
        ext = Path(file_path).suffix.lower()
        if ext not in ['.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg']:
            print(f"⚠️  Unsupported file extension: {ext}")
            return False
        
        # For PDF files, check if it's actually a PDF
        if ext == '.pdf':
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if header != b'%PDF':
                    print("⚠️  File has .pdf extension but may not be a valid PDF")
                    print("Header bytes:", header)
                    return False
                else:
                    print("✅ File is a valid PDF")
                    return True
        else:
            print(f"✅ File extension {ext} is supported")
            return True
            
    except Exception as e:
        print(f"❌ Error checking file type: {e}")
        return False

def test_upload_with_debug(file_path):
    """Test upload with detailed debugging"""
    url = "http://localhost:8000/api/dpr/upload"
    
    print(f"\n📤 Testing upload of: {file_path}")
    
    try:
        # Prepare upload (don't read file content for inspection here)
        with open(file_path, 'rb') as f:
            files = {"file": (os.path.basename(file_path), f, "application/pdf")}
            data = {"uploaded_by": "diagnostic_test"}
            
            print("🚀 Sending upload request...")
            response = requests.post(url, files=files, data=data, timeout=30)
            
            print(f"📊 Status Code: {response.status_code}")
            print(f"📋 Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ Upload successful!")
                try:
                    result = response.json()
                    print("📄 Response Data:")
                    print(json.dumps(result, indent=2))
                except:
                    print("📄 Response Text:")
                    print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            else:
                print(f"❌ Upload failed with status {response.status_code}")
                try:
                    error_result = response.json()
                    print(f"📄 Error Details: {error_result}")
                except:
                    print("📄 Response Text:")
                    print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                    
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
    except requests.exceptions.Timeout:
        print("❌ Upload request timed out")
    except Exception as e:
        print(f"❌ Upload error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

def create_test_pdf():
    """Create a simple test PDF file"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "test_dpr_document.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter
        
        # Add content with better formatting
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 50, "Project Title: Rural Road Development - Phase 2")
        c.drawString(50, height - 90, "Budget Details: ₹30,00,000 (Thirty Lakhs)")
        c.drawString(50, height - 130, "Timeline: 18 months (Jan 2025 - Jun 2026)")
        c.drawString(50, height - 170, "Resources & Manpower: 75 laborers, 8 engineers, 15 vehicles")
        c.drawString(50, height - 210, "Location / Region: Village Rampur to Highway NH-44, District East")
        c.drawString(50, height - 250, "Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon")
        
        c.save()
        print(f"✅ Created test PDF: {filename}")
        return filename
    except ImportError:
        print("⚠️  ReportLab not installed. Creating text file instead.")
        filename = "test_dpr_document.txt"
        with open(filename, "w") as f:
            f.write("""Project Title: Rural Road Development - Phase 2

Budget Details: ₹30,00,000 (Thirty Lakhs)

Timeline: 18 months (Jan 2025 - Jun 2026)

Resources & Manpower: 75 laborers, 8 engineers, 15 vehicles

Location / Region: Village Rampur to Highway NH-44, District East

Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon""")
        print(f"✅ Created test text file: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error creating test file: {e}")
        return None

def main():
    """Main diagnostic function"""
    print("🔍 PDF Upload Diagnostic Tool")
    print("=" * 50)
    
    # Check backend
    if not check_backend_health():
        print("\n🔧 Please start the backend server:")
        print("   cd backend")
        print("   python -m uvicorn main:app --reload --port 8001")
        return
    
    # Get file path from command line or create test file
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("\n📄 No file specified. Creating test file...")
        file_path = create_test_pdf()
        if not file_path:
            print("❌ Failed to create test file")
            return
    
    # Check file
    if not check_file_validity(file_path):
        return
    
    if not check_file_type(file_path):
        print("⚠️  File type check failed, but continuing with upload test...")
    
    # Test upload
    test_upload_with_debug(file_path)
    
    print("\n📝 Diagnostic complete!")

if __name__ == "__main__":
    main()