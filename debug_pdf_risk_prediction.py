import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService
from app.ai.nlp_extractor import NLPExtractor
from app.ai.risk_predictor import RiskPredictor
from app.utils.dpr_processor import extract_text_from_pdf
import json

def debug_pdf_risk_prediction():
    # Initialize services
    ai_service = AIService()
    nlp_extractor = NLPExtractor()
    risk_predictor = RiskPredictor()
    
    # Test with actual PDF files
    pdf_files = [
        "sample_dpr.pdf",
        "Model_DPR_Final 2.0.pdf",
        "BridgesDPRTemplate[1].pdf"
    ]
    
    print("=== DEBUGGING PDF RISK PREDICTION ===\n")
    
    for pdf_file in pdf_files:
        file_path = os.path.join(os.path.dirname(__file__), pdf_file)
        if not os.path.exists(file_path):
            print(f"File not found: {pdf_file}")
            continue
            
        print(f"--- Processing {pdf_file.upper()} ---")
        
        try:
            # Extract text from PDF
            print("\n1. Extracting text from PDF...")
            with open(file_path, "rb") as f:
                pdf_content = f.read()
            text = extract_text_from_pdf(pdf_content)
            print(f"Extracted text length: {len(text)} characters")
            
            # Show first 500 characters of extracted text
            print(f"First 500 characters: {repr(text[:500])}")
            
            # Extract entities
            print("\n2. Extracting entities...")
            extraction = nlp_extractor.extract_entities(text)
            print(f"Project Title: {extraction.project_title}")
            print(f"Estimated Cost: {extraction.estimated_cost}")
            print(f"Duration: {extraction.duration}")
            print(f"Number of Employees: {extraction.num_employees}")
            print(f"Risk Zone: {extraction.risk_zone}")
            print(f"Guidelines Followed: {extraction.guidelines_followed}")
            print(f"Missing Documents Count: {len(extraction.missing_documents) if extraction.missing_documents else 0}")
            
            # Extract features
            print("\n3. Extracting features...")
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
            print("\n4. Predicting risks...")
            risk_scores = risk_predictor.predict_risks(features)
            print("Risk Scores:")
            for risk_type, score in risk_scores.items():
                print(f"  {risk_type}: {score:.4f}")
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    debug_pdf_risk_prediction()