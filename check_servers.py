import requests
import time

def check_servers():
    """
    Check if both backend and frontend servers are running
    """
    print("Checking if servers are running...")
    
    # Check backend server
    try:
        backend_response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if backend_response.status_code == 200:
            print("✅ Backend server is running")
            print(f"   Status: {backend_response.json()}")
        else:
            print("❌ Backend server is not responding correctly")
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend server is not running: {e}")
    
    # Check frontend server
    try:
        frontend_response = requests.get("http://localhost:3001", timeout=5)
        if frontend_response.status_code == 200:
            print("✅ Frontend server is running")
            print(f"   Status: Available at http://localhost:3001")
        else:
            print("❌ Frontend server is not responding correctly")
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend server is not running: {e}")

if __name__ == "__main__":
    check_servers()