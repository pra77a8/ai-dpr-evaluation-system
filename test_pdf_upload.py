import requests

# Test PDF upload directly to backend
def test_pdf_upload():
    try:
        # Use the test PDF that's included in the project
        with open("backend/test_dpr_document.pdf", "rb") as f:
            files = {"file": ("test_dpr_document.pdf", f, "application/pdf")}
            data = {"uploaded_by": "test_user"}
            
            response = requests.post(
                "http://localhost:8000/api/dpr/upload",
                files=files,
                data=data
            )
            
            print("Status Code:", response.status_code)
            print("Response:", response.json())
    except Exception as e:
        print("PDF upload test failed:", str(e))

if __name__ == "__main__":
    test_pdf_upload()