import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import app

def check_routes():
    """Check what routes are available in the app"""
    print("=== AVAILABLE ROUTES ===")
    for route in app.routes:
        print(f"Method: {route.methods} | Path: {route.path} | Name: {route.name}")

if __name__ == "__main__":
    check_routes()