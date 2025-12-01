"""
Full test to upload a DPR, generate reports, and verify download functionality
"""

import requests
import os
import time

def test_full_workflow():
    """Test the full workflow: upload DPR, generate reports, and download them"""
    
    # Test uploading the Model_DPR_Final 2.0.pdf
    pdf_path = "Model_DPR_Final 2.0.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found!")
        return False
    
    print("=== Testing Full DPR Upload and Report Workflow ===")
    
    try:
        # Upload the DPR with AI analysis
        with open(pdf_path, "rb") as f:
            files = {"file": (pdf_path, f, "application/pdf")}
            data = {"uploaded_by": "test_user", "generate_reports": "true"}
            
            print("📤 Uploading DPR with AI analysis...")
            response = requests.post(
                "http://127.0.0.1:8000/api/dpr/upload_with_ai",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ DPR uploaded successfully!")
                
                # Extract DPR ID and report names
                dpr_data = result.get("dpr", {})
                dpr_id = dpr_data.get("id")
                reports = result.get("reports", {})
                
                print(f"   DPR ID: {dpr_id}")
                print(f"   Analytical Report: {reports.get('analytical_report', 'Not generated')}")
                print(f"   Recommendation Report: {reports.get('recommendation_report', 'Not generated')}")
                
                if dpr_id and reports.get('analytical_report') and reports.get('recommendation_report'):
                    # Wait a moment for files to be written to disk
                    time.sleep(2)
                    
                    # Test downloading the analytical report
                    analytical_report_name = reports['analytical_report']
                    print(f"\n📥 Downloading analytical report: {analytical_report_name}")
                    
                    report_response = requests.get(f"http://127.0.0.1:8000/api/dpr/reports/{analytical_report_name}")
                    
                    if report_response.status_code == 200:
                        with open(f"downloaded_{analytical_report_name}", "wb") as report_file:
                            report_file.write(report_response.content)
                        print(f"✅ Analytical report downloaded successfully! ({len(report_response.content)} bytes)")
                    else:
                        print(f"❌ Failed to download analytical report: {report_response.status_code}")
                        print(f"   Response: {report_response.text}")
                        return False
                    
                    # Test downloading the recommendation report
                    recommendation_report_name = reports['recommendation_report']
                    print(f"\n📥 Downloading recommendation report: {recommendation_report_name}")
                    
                    report_response = requests.get(f"http://127.0.0.1:8000/api/dpr/reports/{recommendation_report_name}")
                    
                    if report_response.status_code == 200:
                        with open(f"downloaded_{recommendation_report_name}", "wb") as report_file:
                            report_file.write(report_response.content)
                        print(f"✅ Recommendation report downloaded successfully! ({len(report_response.content)} bytes)")
                    else:
                        print(f"❌ Failed to download recommendation report: {report_response.status_code}")
                        print(f"   Response: {report_response.text}")
                        return False
                    
                    # Test fetching the DPR to verify reports are stored
                    print("\n📋 Fetching DPR to verify reports are stored...")
                    dpr_response = requests.get(f"http://127.0.0.1:8000/api/dpr/{dpr_id}")
                    
                    if dpr_response.status_code == 200:
                        fetched_dpr = dpr_response.json()
                        stored_reports = fetched_dpr.get("reports", {})
                        print(f"✅ DPR fetched successfully!")
                        print(f"   Stored Analytical Report: {stored_reports.get('analytical_report', 'Not stored')}")
                        print(f"   Stored Recommendation Report: {stored_reports.get('recommendation_report', 'Not stored')}")
                        
                        if stored_reports.get('analytical_report') and stored_reports.get('recommendation_report'):
                            print("✅ Reports correctly stored in database!")
                        else:
                            print("⚠️  Reports not stored in database")
                    else:
                        print(f"❌ Failed to fetch DPR: {dpr_response.status_code}")
                    
                    return True
                else:
                    print("❌ Reports were not generated properly")
                    return False
            else:
                print(f"❌ DPR upload failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_full_workflow()
    
    if success:
        print("\n🎉 Full workflow test passed! Report download functionality is working correctly.")
    else:
        print("\n❌ Full workflow test failed. Please check the errors above.")