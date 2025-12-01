import requests
import json

def test_organization_dashboard():
    """Test the organization dashboard endpoint"""
    
    backend_url = "http://localhost:8003"
    
    print("=== TESTING ORGANIZATION DASHBOARD ENDPOINT ===")
    print(f"Backend URL: {backend_url}")
    print()
    
    try:
        # Test the organization dashboard endpoint
        response = requests.get(f"{backend_url}/api/feedback/organization/dashboard", timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Number of feedback items: {len(data)}")
            print()
            
            # Show details of each feedback item
            for i, feedback in enumerate(data[:5]):  # Show first 5 items
                print(f"Feedback #{i+1}:")
                print(f"  ID: {feedback.get('id', 'N/A')}")
                print(f"  DPR ID: {feedback.get('dpr_id', 'N/A')}")
                print(f"  Project Title: {feedback.get('project_title', 'N/A')}")
                print(f"  Civilian Name: {feedback.get('civilian_name', 'N/A')}")
                print(f"  Content: {feedback.get('content', 'N/A')[:50]}...")
                print(f"  Likes: {feedback.get('likes_count', 0)}")
                print(f"  Dislikes: {feedback.get('dislikes_count', 0)}")
                print(f"  Submitted At: {feedback.get('submitted_at', 'N/A')}")
                print()
                
        else:
            print(f"Error: {response.status_code}")
            print(f"Response Text: {response.text}")
            
    except Exception as e:
        print(f"Error testing organization dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_organization_dashboard()