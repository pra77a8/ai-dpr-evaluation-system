import requests
import json

def debug_specific_dpr():
    """Debug a specific DPR to see what data it contains"""
    
    backend_url = "http://localhost:8004"
    
    print("=== DEBUGGING SPECIFIC DPR ===")
    print(f"Backend URL: {backend_url}")
    print()
    
    # Let's check a specific DPR ID that we know should have data
    # From our previous tests, DPR ID 68e3e712dcb4b0dfc62026e3 should have good data
    dpr_id = "68e3e712dcb4b0dfc62026e3"
    
    try:
        # Test getting specific DPR
        response = requests.get(f"{backend_url}/api/dpr/{dpr_id}", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("DPR Data:")
            print(json.dumps(data, indent=2, default=str))
            
        else:
            print(f"Error getting DPR: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Error testing specific DPR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Also test the AI analysis endpoint
    try:
        response = requests.post(f"{backend_url}/api/dpr/{dpr_id}/analyze_with_ai", timeout=30)
        
        print(f"AI Analysis Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("AI Analysis Data:")
            print(json.dumps(data, indent=2, default=str))
            
        else:
            print(f"Error with AI analysis: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Error testing AI analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_specific_dpr()