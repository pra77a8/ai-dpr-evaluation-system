import requests
import time

def check_backend():
    """Check if the backend is accessible"""
    urls = [
        "http://localhost:8000/",
        "http://localhost:8000/health",
        "http://localhost:8000/docs"
    ]
    
    for url in urls:
        try:
            print(f"Checking {url}...")
            response = requests.get(url, timeout=5)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print("  SUCCESS!")
            else:
                print(f"  Response: {response.text[:100]}...")
        except requests.exceptions.ConnectionError:
            print("  ERROR: Cannot connect to backend")
        except requests.exceptions.Timeout:
            print("  ERROR: Request timed out")
        except Exception as e:
            print(f"  ERROR: {e}")
        print()

if __name__ == "__main__":
    print("Checking backend server accessibility...")
    print("=" * 50)
    check_backend()