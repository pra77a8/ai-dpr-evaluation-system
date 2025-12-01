import requests

# Test PDF upload with Model DPR file
def test_model_dpr_upload():
    try:
        # Use the Model DPR file that's included in the project
        with open("Model_DPR_Final 2.0.pdf", "rb") as f:
            files = {"file": ("Model_DPR_Final 2.0.pdf", f, "application/pdf")}
            data = {"uploaded_by": "test_user"}
            
            response = requests.post(
                "http://localhost:8000/api/dpr/upload",
                files=files,
                data=data
            )
            
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                print("Response:", response.json())
            else:
                print("Error Response:", response.text)
    except Exception as e:
        print("PDF upload test failed:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_dpr_upload()