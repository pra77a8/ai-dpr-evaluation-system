import requests

def test_basic_upload():
    """Test basic DPR upload"""
    url = "http://127.0.0.1:8000/api/dpr/upload"
    
    with open("Model_DPR_Final 2.0.pdf", "rb") as f:
        files = {"file": ("Model_DPR_Final 2.0.pdf", f, "application/pdf")}
        data = {"uploaded_by": "test_user"}
        
        print("Uploading DPR...")
        response = requests.post(url, files=files, data=data)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            print(response.json())
        else:
            print("Error:")
            print(response.text)

if __name__ == "__main__":
    test_basic_upload()