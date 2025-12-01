from pymongo import MongoClient
from pprint import pprint

def check_mongodb_structure():
    """
    Connect to MongoDB and check the database structure
    """
    try:
        # Connect to MongoDB (using default localhost:27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Access the DPR evaluation system database
        db = client['dpr_evaluation_system']
        
        print("=== DATABASE STRUCTURE ===")
        print(f"Database name: dpr_evaluation_system")
        
        # List all collections
        collections = db.list_collection_names()
        print(f"\nCollections: {collections}")
        
        # Check each collection
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({})
            print(f"\n--- Collection: {collection_name} ({count} documents) ---")
            
            # Show first document as example (if collection is not empty)
            if count > 0:
                first_doc = collection.find_one()
                print("Sample document structure:")
                pprint(first_doc, indent=2, width=80, depth=3)
                
                # Show field names from the first document
                if first_doc:
                    print("\nFields in collection:")
                    for field in first_doc.keys():
                        print(f"  - {field}")
            else:
                print("  (Empty collection)")
        
        # Close connection
        client.close()
        print("\n=== CONNECTION CLOSED ===")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

if __name__ == "__main__":
    check_mongodb_structure()