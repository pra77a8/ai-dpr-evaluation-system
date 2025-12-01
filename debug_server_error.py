"""
Debug the server error by testing the components directly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_components():
    """Test individual components to identify the issue"""
    print("=== Debugging Server Error ===")
    
    # Test 1: Import all components
    print("\n1. Testing Component Imports:")
    try:
        from app.ai.ai_service import AIService
        print("✅ AI Service imported successfully")
    except Exception as e:
        print(f"❌ AI Service import failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        from app.utils.dpr_processor import extract_dpr_elements
        print("✅ DPR Processor imported successfully")
    except Exception as e:
        print(f"❌ DPR Processor import failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Initialize AI Service
    print("\n2. Testing AI Service Initialization:")
    try:
        ai_service = AIService()
        print("✅ AI Service initialized successfully")
    except Exception as e:
        print(f"❌ AI Service initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Test extraction with sample text
    print("\n3. Testing Extraction with Sample Text:")
    sample_text = "Project Title: Test Project\nBudget: ₹10,00,000\nDuration: 12 months"
    
    try:
        result = ai_service.extract_dpr_entities(sample_text)
        print(f"✅ Extraction successful: {result.project_title}")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 4: Test DPR processor
    print("\n4. Testing DPR Processor:")
    try:
        dpr_result = extract_dpr_elements(sample_text)
        print(f"✅ DPR Processor successful: {dpr_result.project_title}")
    except Exception as e:
        print(f"❌ DPR Processor failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n🎉 All tests passed! Components are working correctly.")

if __name__ == "__main__":
    test_components()