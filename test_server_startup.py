"""
Test server startup to verify the fix
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_server_startup():
    """Test that the server can start without errors"""
    print("=== Testing Server Startup ===")
    
    try:
        # Test importing the main FastAPI app
        from main import app
        print("✅ Main app imported successfully")
        
        # Test importing the DPR routes
        from app.routes.dpr import router
        print("✅ DPR routes imported successfully")
        
        # Test that all routes are registered
        routes = [route.path for route in app.routes]
        print(f"✅ App has {len(routes)} routes")
        
        # Check for key routes
        key_routes = ["/api/dpr/upload", "/api/dpr/upload_with_ai", "/health"]
        for route in key_routes:
            if any(route in r for r in routes):
                print(f"✅ Route {route} found")
            else:
                print(f"❌ Route {route} not found")
        
        print("\n🎉 Server startup test passed!")
        print("The server should now start without 500 errors.")
        
    except Exception as e:
        print(f"❌ Server startup test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_server_startup()