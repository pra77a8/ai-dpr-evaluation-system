"""
Simple import test
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def simple_test():
    """Simple test"""
    print("Testing imports...")
    
    try:
        from app.routes.dpr import router
        print("✅ DPR routes imported successfully")
    except Exception as e:
        print(f"❌ DPR routes import failed: {e}")
        import traceback
        traceback.print_exc()
        return
        
    try:
        from main import app
        print("✅ Main app imported successfully")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        import traceback
        traceback.print_exc()
        return
        
    print("SUCCESS!")

if __name__ == "__main__":
    simple_test()