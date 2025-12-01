import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService
from app.ai.nlp_extractor import NLPExtractor
from app.ai.risk_predictor import RiskPredictor
from app.models.ai_models import EnhancedDPRExtraction
import json

def debug_risk_prediction():
    # Initialize services
    ai_service = AIService()
    nlp_extractor = NLPExtractor()
    risk_predictor = RiskPredictor()
    
    # Test with different sample texts
    sample_texts = {
        "sample_dpr": """
Project: Rural Road Development - Phase 2
Department: Public Works Department
Region: Northeast India
Duration: 18 months
Estimated Cost: ₹150 crore
Fund Allocation: ₹140 crore
Contingency: ₹10 crore
Start Date: 01/06/2024
End Date: 01/12/2025
Number of Employees: 150
State: Assam
District: Guwahati
Risk Zone: Flood prone area
Engineering Details: Standard road construction specifications
Guidelines Followed: Yes
        """,
        "model_dpr": """
DETAILED PROJECT REPORT (DPR)
For
Roll-Out of National e-Vidhan Application(NeVA)
In
Ministry of Parliamentary Affairs
Project Tentative Outlay: Rs XX,XX,XX,XXX
Duration: 24 months
Number of Employees: 75
State: Delhi
District: New Delhi
Risk Zone: Connectivity issues
Guidelines Followed: Yes
        """,
        "bridges_dpr": """
Project Title: Construction of New Bridge over Brahmaputra River
Department: Road Construction Department
Region: Northeast India
Duration: 36 months
Estimated Cost: ₹300 crore
Fund Allocation: ₹270 crore
Contingency: ₹30 crore
Start Date: 15/03/2024
End Date: 15/03/2027
Number of Employees: 200
State: Assam
District: Guwahati
Risk Zone: Flood and landslide prone area
Engineering Details: Bridge construction specifications
Guidelines Followed: Yes
        """
    }
    
    print("=== DEBUGGING RISK PREDICTION ===\n")
    
    for name, text in sample_texts.items():
        print(f"--- Processing {name.upper()} ---")
        
        # Extract entities
        print("\n1. Extracting entities...")
        extraction = nlp_extractor.extract_entities(text)
        print(f"Project Title: {extraction.project_title}")
        print(f"Estimated Cost: {extraction.estimated_cost}")
        print(f"Duration: {extraction.duration}")
        print(f"Number of Employees: {extraction.num_employees}")
        print(f"Risk Zone: {extraction.risk_zone}")
        print(f"Guidelines Followed: {extraction.guidelines_followed}")
        print(f"Missing Documents Count: {len(extraction.missing_documents) if extraction.missing_documents else 0}")
        
        # Extract features
        print("\n2. Extracting features...")
        features = {
            'contingency_ratio': ai_service._calculate_contingency_ratio(extraction),
            'duration_months': ai_service._extract_duration_months(extraction),
            'num_employees': extraction.num_employees or 50,
            'num_machinery': len(extraction.machinery) if extraction.machinery else 3,
            'num_materials': len(extraction.materials) if extraction.materials else 5,
            'compliance_score': 1 if extraction.guidelines_followed else 0,
            'missing_docs_count': len(extraction.missing_documents) if extraction.missing_documents else 0
        }
        print("Features:")
        for key, value in features.items():
            print(f"  {key}: {value}")
        
        # Predict risks
        print("\n3. Predicting risks...")
        risk_scores = risk_predictor.predict_risks(features)
        print("Risk Scores:")
        for risk_type, score in risk_scores.items():
            print(f"  {risk_type}: {score:.4f}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    debug_risk_prediction()