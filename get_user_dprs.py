import requests
import json

def get_user_dprs():
    """Get DPRs for a user and check for reports"""
    url = "http://127.0.0.1:8000/api/dpr/user/test_user"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            dprs = response.json()
            print(f"Found {len(dprs)} DPRs")
            
            for i, dpr in enumerate(dprs):
                print(f"\n--- DPR {i+1} ---")
                print(f"ID: {dpr.get('id')}")
                print(f"File Name: {dpr.get('file_name')}")
                print(f"Project Title: {dpr.get('extracted_data', {}).get('project_title')}")
                
                # Check for reports
                reports = dpr.get('reports')
                if reports:
                    print(f"Reports: {reports}")
                else:
                    print("No reports found")
                    
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    get_user_dprs()