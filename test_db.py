"""
Test database connection and basic operations
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import get_dprs_collection
from datetime import datetime

def test_database_connection():
    """Test database connection and basic operations"""
    try:
        print("Testing database connection...")
        dprs_collection = get_dprs_collection()
        
        # Test inserting a document
        test_doc = {
            "file_name": "test_document.pdf",
            "file_type": "pdf",
            "uploaded_by": "test_user",
            "extracted_data": {
                "project_title": "Test Project"
            },
            "uploaded_at": datetime.utcnow()
        }
        
        result = dprs_collection.insert_one(test_doc)
        print(f"✅ Insert successful. ID: {result.inserted_id}")
        
        # Test finding the document
        found_doc = dprs_collection.find_one({"_id": result.inserted_id})
        if found_doc:
            print(f"✅ Find successful. Project Title: {found_doc.get('extracted_data', {}).get('project_title')}")
        else:
            print("❌ Find failed")
            
        # Test deleting the document
        delete_result = dprs_collection.delete_one({"_id": result.inserted_id})
        print(f"✅ Delete successful. Deleted count: {delete_result.deleted_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    
    if success:
        print("\n✅ Database connection test passed!")
    else:
        print("\n❌ Database connection test failed!")