from pymongo import MongoClient
from pprint import pprint
import json

def check_ai_enhanced_data():
    """
    Check for AI-enhanced data structures in MongoDB
    """
    try:
        # Connect to MongoDB (using default localhost:27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Access the DPR evaluation system database
        db = client['dpr_evaluation_system']
        
        print("=== CHECKING FOR AI-ENHANCED DATA STRUCTURES ===")
        
        # Check DPRs collection for enhanced extraction data
        dprs_collection = db['dprs']
        count = dprs_collection.count_documents({})
        print(f"\nDPRs collection: {count} documents")
        
        # Look for documents with enhanced_extraction field
        enhanced_count = dprs_collection.count_documents({"enhanced_extraction": {"$exists": True}})
        print(f"Documents with enhanced_extraction: {enhanced_count}")
        
        # Look for documents with AI risk scores
        ai_risk_count = dprs_collection.count_documents({"ai_risk_scores": {"$exists": True}})
        print(f"Documents with AI risk scores: {ai_risk_count}")
        
        # Look for documents with completeness score
        completeness_count = dprs_collection.count_documents({"completeness_score": {"$exists": True}})
        print(f"Documents with completeness score: {completeness_count}")
        
        # Look for documents with recommendations
        recommendations_count = dprs_collection.count_documents({"recommendations": {"$exists": True}})
        print(f"Documents with recommendations: {recommendations_count}")
        
        # Show a sample of enhanced data if available
        if enhanced_count > 0:
            print("\n--- Sample Enhanced Extraction Data ---")
            sample_doc = dprs_collection.find_one({"enhanced_extraction": {"$exists": True}})
            if sample_doc and "enhanced_extraction" in sample_doc:
                print("Enhanced extraction fields:")
                for key, value in sample_doc["enhanced_extraction"].items():
                    value_type = type(value).__name__
                    if isinstance(value, list) and len(value) > 0:
                        print(f"  {key}: Array of {type(value[0]).__name__} ({len(value)} items)")
                    elif isinstance(value, list):
                        print(f"  {key}: Empty Array")
                    else:
                        print(f"  {key}: {value_type} = {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
        
        # Check risks collection for AI-enhanced data
        risks_collection = db['risks']
        risks_count = risks_collection.count_documents({})
        print(f"\nRisks collection: {risks_count} documents")
        
        # Look for documents with completeness score
        risks_completeness_count = risks_collection.count_documents({"completeness_score": {"$exists": True}})
        print(f"Risk documents with completeness score: {risks_completeness_count}")
        
        # Look for documents with recommendations
        risks_recommendations_count = risks_collection.count_documents({"recommendations": {"$exists": True}})
        print(f"Risk documents with recommendations: {risks_recommendations_count}")
        
        # Close connection
        client.close()
        print(f"\n=== ANALYSIS COMPLETE ===")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_ai_enhanced_data()