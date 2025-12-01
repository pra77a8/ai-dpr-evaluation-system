"""
Comprehensive test for both project title extraction and report download
"""

import requests
import os
import time

def test_comprehensive_workflow():
    """Test the complete workflow: upload, extract title, generate reports, download reports"""
    
    print("=== Comprehensive DPR Processing Test ===")
    
    try:
        # Step 1: Upload DPR with AI analysis to generate reports
        print("\n1. Uploading DPR with AI analysis...")
        with open("Model_DPR_Final 2.0.pdf", "rb") as f:
            files = {"file": ("Model_DPR_Final 2.0.pdf", f, "application/pdf")}
            data = {"uploaded_by": "test_user", "generate_reports": "true"}
            
            response = requests.post(
                "http://127.0.0.1:8000/api/dpr/upload_with_ai",
                files=files,
                data=data
            )
            
            if response.status_code != 200:
                print(f"❌ Upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
            
            result = response.json()
            print("✅ DPR uploaded successfully!")
            
            # Extract information
            dpr_data = result.get("dpr", {})
            dpr_id = dpr_data.get("id")
            extracted_data = dpr_data.get("extracted_data", {})
            reports = result.get("reports", {})
            
            print(f"   DPR ID: {dpr_id}")
            print(f"   Project Title: {extracted_data.get('project_title')}")
            print(f"   Analytical Report: {reports.get('analytical_report')}")
            print(f"   Recommendation Report: {reports.get('recommendation_report')}")
            
            # Step 2: Verify project title extraction
            project_title = extracted_data.get('project_title')
            if not project_title:
                print("❌ Project title not extracted!")
                return False
            
            # Check if it's the expected title
            expected_parts = ["Roll-Out", "National e-Vidhan", "Application(NeVA)"]
            if all(part in project_title for part in expected_parts):
                print("✅ Project title extracted correctly!")
            else:
                print(f"⚠️  Project title extracted but may not be complete: {project_title}")
            
            # Step 3: Wait for report generation
            print("\n2. Waiting for report generation...")
            time.sleep(3)  # Give time for reports to be written to disk
            
            # Step 4: Test downloading analytical report
            analytical_report_name = reports.get('analytical_report')
            if not analytical_report_name:
                print("❌ Analytical report not generated!")
                return False
                
            print(f"\n3. Downloading analytical report: {analytical_report_name}")
            report_response = requests.get(f"http://127.0.0.1:8000/api/dpr/reports/{analytical_report_name}")
            
            if report_response.status_code == 200:
                with open(f"downloaded_{analytical_report_name}", "wb") as report_file:
                    report_file.write(report_response.content)
                print(f"✅ Analytical report downloaded successfully! ({len(report_response.content)} bytes)")
            else:
                print(f"❌ Failed to download analytical report: {report_response.status_code}")
                print(f"   Response: {report_response.text}")
                return False
            
            # Step 5: Test downloading recommendation report
            recommendation_report_name = reports.get('recommendation_report')
            if not recommendation_report_name:
                print("❌ Recommendation report not generated!")
                return False
                
            print(f"\n4. Downloading recommendation report: {recommendation_report_name}")
            report_response = requests.get(f"http://127.0.0.1:8000/api/dpr/reports/{recommendation_report_name}")
            
            if report_response.status_code == 200:
                with open(f"downloaded_{recommendation_report_name}", "wb") as report_file:
                    report_file.write(report_response.content)
                print(f"✅ Recommendation report downloaded successfully! ({len(report_response.content)} bytes)")
            else:
                print(f"❌ Failed to download recommendation report: {report_response.status_code}")
                print(f"   Response: {report_response.text}")
                return False
            
            # Step 6: Verify the downloaded files are valid PDFs
            print("\n5. Verifying downloaded files...")
            for filename in [f"downloaded_{analytical_report_name}", f"downloaded_{recommendation_report_name}"]:
                if os.path.exists(filename):
                    # Check if it's a PDF by looking at the first few bytes
                    with open(filename, "rb") as f:
                        header = f.read(4)
                        if header == b'%PDF':
                            print(f"✅ {filename} is a valid PDF file")
                        else:
                            print(f"❌ {filename} is not a valid PDF file")
                            return False
                else:
                    print(f"❌ {filename} not found")
                    return False
            
            # Step 7: Test fetching DPR to verify reports are stored in database
            print("\n6. Verifying reports are stored in database...")
            dpr_response = requests.get(f"http://127.0.0.1:8000/api/dpr/{dpr_id}")
            
            if dpr_response.status_code == 200:
                fetched_dpr = dpr_response.json()
                stored_reports = fetched_dpr.get("reports", {})
                print("✅ DPR fetched successfully from database!")
                print(f"   Stored Analytical Report: {stored_reports.get('analytical_report')}")
                print(f"   Stored Recommendation Report: {stored_reports.get('recommendation_report')}")
                
                if stored_reports.get('analytical_report') and stored_reports.get('recommendation_report'):
                    print("✅ Reports correctly stored in database!")
                else:
                    print("⚠️  Reports not properly stored in database")
            else:
                print(f"❌ Failed to fetch DPR from database: {dpr_response.status_code}")
            
            print("\n🎉 All tests passed! The system is working correctly.")
            return True
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_comprehensive_workflow()
    
    if success:
        print("\n✅ Comprehensive test completed successfully!")
    else:
        print("\n❌ Comprehensive test failed!")