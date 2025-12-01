import requests

# Test PDF upload with Bridges DPR template
def test_bridges_dpr_upload():
    try:
        # Use the Bridges DPR template that's included in the project
        with open("BridgesDPRTemplate[1].pdf", "rb") as f:
            files = {"file": ("BridgesDPRTemplate[1].pdf", f, "application/pdf")}
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
    test_bridges_dpr_upload()