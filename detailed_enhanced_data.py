from pymongo import MongoClient
import json

def detailed_enhanced_data():
    """
    Show detailed enhanced extraction data
    """
    try:
        # Connect to MongoDB (using default localhost:27017)
        client = MongoClient('mongodb://localhost:27017/')
        
        # Access the DPR evaluation system database
        db = client['dpr_evaluation_system']
        
        print("=== DETAILED ENHANCED EXTRACTION DATA ===")
        
        # Find a document with enhanced extraction
        dprs_collection = db['dprs']
        sample_doc = dprs_collection.find_one({"enhanced_extraction": {"$exists": True}})
        
        if sample_doc:
            print(f"\nDocument ID: {sample_doc['_id']}")
            print(f"File name: {sample_doc['file_name']}")
            print(f"Uploaded by: {sample_doc['uploaded_by']}")
            print(f"Uploaded at: {sample_doc['uploaded_at']}")
            
            print("\n--- ENHANCED EXTRACTION DATA ---")
            enhanced_data = sample_doc['enhanced_extraction']
            
            # Print key fields with their values
            key_fields = [
                'project_title', 'department', 'estimated_cost', 'duration', 
                'state', 'district', 'num_employees', 'guidelines_followed'
            ]
            
            for field in key_fields:
                value = enhanced_data.get(field, 'N/A')
                print(f"{field}: {value}")
            
            # Show array fields
            print(f"\nMilestones ({len(enhanced_data.get('milestones', []))} items):")
            for i, milestone in enumerate(enhanced_data.get('milestones', [])[:5]):
                print(f"  {i+1}. {milestone}")
            if len(enhanced_data.get('milestones', [])) > 5:
                print(f"  ... and {len(enhanced_data.get('milestones', [])) - 5} more")
                
            print(f"\nMachinery ({len(enhanced_data.get('machinery', []))} items):")
            for i, machine in enumerate(enhanced_data.get('machinery', [])[:5]):
                print(f"  {i+1}. {machine}")
            if len(enhanced_data.get('machinery', [])) > 5:
                print(f"  ... and {len(enhanced_data.get('machinery', [])) - 5} more")
                
            print(f"\nMaterials ({len(enhanced_data.get('materials', []))} items):")
            for i, material in enumerate(enhanced_data.get('materials', [])[:5]):
                print(f"  {i+1}. {material}")
            if len(enhanced_data.get('materials', [])) > 5:
                print(f"  ... and {len(enhanced_data.get('materials', [])) - 5} more")
            
            # Show risk zone and environmental info
            print(f"\nRisk zone: {enhanced_data.get('risk_zone', 'N/A')}")
            print(f"Environmental risks: {enhanced_data.get('environmental_risks', 'N/A')}")
            
            # Show technical details
            eng_details = enhanced_data.get('engineering_details', 'N/A')
            print(f"\nEngineering details: {eng_details[:200]}{'...' if len(eng_details) > 200 else ''}")
            
            specs = enhanced_data.get('specifications', 'N/A')
            print(f"Specifications: {specs[:200]}{'...' if len(specs) > 200 else ''}")
            
        else:
            print("No documents with enhanced extraction found")
        
        # Close connection
        client.close()
        print(f"\n=== ANALYSIS COMPLETE ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    detailed_enhanced_data()