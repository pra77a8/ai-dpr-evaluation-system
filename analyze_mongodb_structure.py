from pymongo import MongoClient
from pprint import pprint
import json

def analyze_mongodb_structure():
    """
    Connect to MongoDB and analyze the database structure in detail
    """
    try:
        # Connect to MongoDB (using default localhost:27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Access the DPR evaluation system database
        db = client['dpr_evaluation_system']
        
        print("=== DETAILED DATABASE STRUCTURE ANALYSIS ===")
        print(f"Database name: dpr_evaluation_system")
        
        # List all collections
        collections = db.list_collection_names()
        print(f"\nCollections: {collections}")
        
        # Analyze each collection in detail
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"\n{'='*50}")
            print(f"COLLECTION: {collection_name.upper()}")
            print(f"Document count: {count}")
            print(f"{'='*50}")
            
            if count > 0:
                # Show first few documents
                print("\nSample documents:")
                cursor = collection.find().limit(2)
                for i, doc in enumerate(cursor, 1):
                    print(f"\n--- Document {i} ---")
                    # Pretty print with better formatting
                    print(json.dumps(doc, default=str, indent=2))
                
                # Analyze field structure
                print(f"\n--- Field Analysis ---")
                # Get a sample document to analyze fields
                sample_doc = collection.find_one()
                analyze_document_fields(sample_doc, "")
            else:
                print("  (Empty collection)")
        
        # Close connection
        client.close()
        print(f"\n{'='*50}")
        print("ANALYSIS COMPLETE")
        print(f"{'='*50}")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

def analyze_document_fields(doc, prefix=""):
    """
    Recursively analyze document fields and their types
    """
    if not doc:
        return
        
    for key, value in doc.items():
        field_path = f"{prefix}.{key}" if prefix else key
        
        if isinstance(value, dict):
            print(f"  {field_path}: Object (embedded document)")
            # Recursively analyze nested fields
            analyze_document_fields(value, field_path)
        elif isinstance(value, list):
            if value:
                element_type = type(value[0]).__name__
                print(f"  {field_path}: Array of {element_type}")
            else:
                print(f"  {field_path}: Empty Array")
        else:
            value_type = type(value).__name__
            print(f"  {field_path}: {value_type}")

if __name__ == "__main__":
    analyze_mongodb_structure()