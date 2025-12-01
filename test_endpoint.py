import requests

def test_report_endpoint():
    """Test the report download endpoint"""
    url = "http://127.0.0.1:8000/api/dpr/reports/68e37c14f42881a132dcc54c_Heatmap_Analysis.pdf"
    
    print("Testing report download endpoint...")
    try:
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type')}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Endpoint is working!")
            # Save the file to verify it's a valid PDF
            with open("test_endpoint_download.pdf", "wb") as f:
                f.write(response.content)
            print("✅ File saved as test_endpoint_download.pdf")
            return True
        else:
            print("❌ Endpoint failed")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_report_endpoint()