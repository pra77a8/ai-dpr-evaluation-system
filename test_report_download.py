"""
Test script to verify report download functionality
"""

import requests
import os

def test_report_download():
    """Test downloading a report PDF"""
    # Test URL for the report download endpoint
    report_filename = "68e37c14f42881a132dcc54c_Heatmap_Analysis.pdf"
    url = f"http://127.0.0.1:8000/api/dpr/reports/{report_filename}"
    
    print(f"Testing download of report: {report_filename}")
    
    try:
        # Make request to download the report
        response = requests.get(url)
        
        if response.status_code == 200:
            # Save the PDF to a local file
            with open(f"test_{report_filename}", "wb") as f:
                f.write(response.content)
            
            print(f"✅ Report downloaded successfully!")
            print(f"   File size: {len(response.content)} bytes")
            print(f"   Saved as: test_{report_filename}")
            
            # Verify it's a PDF
            if response.headers.get('content-type', '').startswith('application/pdf'):
                print("✅ File is correctly identified as PDF")
            else:
                print("⚠️  File may not be a PDF based on content-type header")
                
            return True
        else:
            print(f"❌ Download failed with status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during download: {str(e)}")
        return False

def test_recommendations_report():
    """Test downloading the recommendations report"""
    report_filename = "68e37c14f42881a132dcc54c_Recommendations_Report.pdf"
    url = f"http://127.0.0.1:8000/api/dpr/reports/{report_filename}"
    
    print(f"\nTesting download of recommendations report: {report_filename}")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(f"test_{report_filename}", "wb") as f:
                f.write(response.content)
            
            print(f"✅ Recommendations report downloaded successfully!")
            print(f"   File size: {len(response.content)} bytes")
            print(f"   Saved as: test_{report_filename}")
            return True
        else:
            print(f"❌ Download failed with status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during download: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Report Download Test ===")
    
    # Test heatmap analysis report
    success1 = test_report_download()
    
    # Test recommendations report
    success2 = test_recommendations_report()
    
    if success1 and success2:
        print("\n✅ All report downloads successful!")
    else:
        print("\n❌ Some downloads failed. Check the errors above.")