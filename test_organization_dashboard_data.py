import requests
import json

def test_organization_dashboard_data():
    """Test the organization dashboard data endpoint"""
    
    backend_url = "http://localhost:8004"
    
    print("=== TESTING ORGANIZATION DASHBOARD DATA ENDPOINT ===")
    print(f"Backend URL: {backend_url}")
    print()
    
    try:
        # Test the organization dashboard endpoint
        response = requests.get(f"{backend_url}/api/dpr/organization/dashboard", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of DPR items: {len(data)}")
            print()
            
            # Show details of each DPR item
            project_titles = {}
            for i, dpr in enumerate(data[:10]):  # Show first 10 items
                print(f"DPR #{i+1}:")
                print(f"  ID: {dpr.get('id', 'N/A')}")
                print(f"  File Name: {dpr.get('file_name', 'N/A')}")
                print(f"  Uploaded By: {dpr.get('uploaded_by', 'N/A')}")
                print(f"  Uploaded At: {dpr.get('uploaded_at', 'N/A')}")
                
                # Extracted data
                extracted_data = dpr.get('enhanced_extraction', {})
                print(f"  Project Title: {extracted_data.get('project_title', 'N/A')}")
                print(f"  Department: {extracted_data.get('department', 'N/A')}")
                print(f"  Estimated Cost: {extracted_data.get('estimated_cost', 'N/A')}")
                print(f"  Duration: {extracted_data.get('duration', 'N/A')}")
                
                # Track project titles
                title = extracted_data.get('project_title', 'N/A')
                if title in project_titles:
                    project_titles[title] += 1
                else:
                    project_titles[title] = 1
                
                print()
            
            # Analyze project titles
            print("Project Title Analysis:")
            print("-" * 30)
            for title, count in project_titles.items():
                if count > 1:
                    print(f"  ⚠ '{title}' appears {count} times")
                else:
                    print(f"  ✓ '{title}' appears {count} time")
            
            print()
            print("=== TEST COMPLETE ===")
                
        else:
            print(f"Error: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Error testing organization dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_organization_dashboard_data()