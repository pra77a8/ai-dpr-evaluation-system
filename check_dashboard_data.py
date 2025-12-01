import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import get_dprs_collection, get_risks_collection
from bson import ObjectId
import json
from datetime import datetime

def check_dashboard_data():
    """Check what data is stored in the database for dashboard display"""
    
    print("=== DASHBOARD DATA ANALYSIS ===")
    print()
    
    # Check DPRs collection
    dprs_collection = get_dprs_collection()
    dprs = list(dprs_collection.find().sort("uploaded_at", -1).limit(10))
    
    print(f"Found {len(dprs)} DPR documents:")
    print("-" * 50)
    
    for i, dpr in enumerate(dprs):
        print(f"DPR #{i+1}:")
        print(f"  ID: {dpr.get('id', dpr.get('_id', 'N/A'))}")
        print(f"  File Name: {dpr.get('file_name', 'N/A')}")
        print(f"  Uploaded By: {dpr.get('uploaded_by', 'N/A')}")
        print(f"  Uploaded At: {dpr.get('uploaded_at', 'N/A')}")
        
        # Extracted data
        extracted_data = dpr.get('enhanced_extraction', {})
        print(f"  Project Title: {extracted_data.get('project_title', 'N/A')}")
        print(f"  Department: {extracted_data.get('department', 'N/A')}")
        print(f"  Estimated Cost: {extracted_data.get('estimated_cost', 'N/A')}")
        print(f"  Duration: {extracted_data.get('duration', 'N/A')}")
        
        # Risk scores if available
        if 'ai_risk_scores' in dpr:
            risk_scores = dpr.get('ai_risk_scores', {})
            print(f"  Risk Scores: {risk_scores}")
        
        print()
    
    # Check risks collection
    risks_collection = get_risks_collection()
    risks = list(risks_collection.find().sort("calculated_at", -1).limit(10))
    
    print(f"Found {len(risks)} Risk documents:")
    print("-" * 50)
    
    for i, risk in enumerate(risks):
        print(f"Risk #{i+1}:")
        print(f"  DPR ID: {risk.get('dpr_id', 'N/A')}")
        print(f"  Project Title: {risk.get('project_title', 'N/A')}")
        print(f"  Calculated At: {risk.get('calculated_at', 'N/A')}")
        print(f"  Risk Scores: {risk.get('risk_scores', {})}")
        print()
    
    # Check if there are duplicate project titles
    project_titles = {}
    for dpr in dprs:
        extracted_data = dpr.get('enhanced_extraction', {})
        title = extracted_data.get('project_title', 'N/A')
        if title in project_titles:
            project_titles[title] += 1
        else:
            project_titles[title] = 1
    
    print("Project Title Analysis:")
    print("-" * 30)
    for title, count in project_titles.items():
        if count > 1:
            print(f"  ⚠ '{title}' appears {count} times")
        else:
            print(f"  ✓ '{title}' appears {count} time")
    
    print()
    print("=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    check_dashboard_data()