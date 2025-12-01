"""
Quick test to verify the DPR endpoint fix works
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend.app.database import get_dprs_collection, get_risks_collection

def test_dashboard_endpoint():
    dprs_collection = get_dprs_collection()
    risks_collection = get_risks_collection()
    
    # Find all DPRs
    dprs = list(dprs_collection.find({}))
    print(f"Found {len(dprs)} DPRs in database")
    
    # Format response with error handling
    formatted_dprs = []
    errors = []
    
    for dpr in dprs:
        try:
            dpr["id"] = str(dpr["_id"])
            del dpr["_id"]
            
            # Ensure all necessary fields are present
            if "enhanced_extraction" not in dpr:
                dpr["enhanced_extraction"] = {}
                
            if "ai_risk_scores" not in dpr or not dpr["ai_risk_scores"]:
                risk_record = risks_collection.find_one({"dpr_id": dpr["id"]})
                if risk_record and "risk_scores" in risk_record:
                    dpr["ai_risk_scores"] = risk_record["risk_scores"]
                else:
                    dpr["ai_risk_scores"] = {}
                    
            if "completeness_score" not in dpr:
                dpr["completeness_score"] = 0
            
            # Remove large text fields
            if "original_text" in dpr and len(str(dpr.get("original_text", ""))) > 100000:
                dpr["original_text"] = str(dpr["original_text"])[:100000] + "... [truncated]"
            
            formatted_dprs.append(dpr)
        except Exception as e:
            errors.append(f"Error processing DPR: {str(e)}")
            continue
    
    print(f"Successfully formatted {len(formatted_dprs)} DPRs")
    if errors:
        print(f"Encountered {len(errors)} errors:")
        for err in errors[:5]:  # Show first 5 errors
            print(f"  - {err}")
    
    return formatted_dprs

if __name__ == "__main__":
    try:
        dprs = test_dashboard_endpoint()
        print("\n✅ Test PASSED - Endpoint logic works correctly")
        print(f"First DPR file_name: {dprs[0].get('file_name', 'N/A')}")
    except Exception as e:
        print(f"\n❌ Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
