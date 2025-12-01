import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.ai_service import AIService
from app.utils.dpr_processor import extract_text_from_pdf
import json

def debug_full_dpr_processing():
    # Initialize services
    ai_service = AIService()
    
    # Test with actual PDF files
    pdf_files = [
        "sample_dpr.pdf",
        "Model_DPR_Final 2.0.pdf",
        "BridgesDPRTemplate[1].pdf"
    ]
    
    print("=== DEBUGGING FULL DPR PROCESSING ===\n")
    
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
            
            # Process DPR completely
            print("\n2. Processing DPR completely...")
            extraction, risk_scores, recommendations = ai_service.process_dpr_completely("test_dpr", text)
            
            # Show extraction results
            print("\n3. Extraction Results:")
            print(f"Project Title: {extraction.project_title}")
            print(f"Department: {extraction.department}")
            print(f"Estimated Cost: {extraction.estimated_cost}")
            print(f"Duration: {extraction.duration}")
            print(f"Number of Employees: {extraction.num_employees}")
            print(f"Risk Zone: {extraction.risk_zone}")
            print(f"Guidelines Followed: {extraction.guidelines_followed}")
            print(f"Missing Documents Count: {len(extraction.missing_documents) if extraction.missing_documents else 0}")
            
            # Show features used for risk prediction
            print("\n4. Features for Risk Prediction:")
            features = {
                'contingency_ratio': ai_service._calculate_contingency_ratio(extraction),
                'duration_months': ai_service._extract_duration_months(extraction),
                'num_employees': extraction.num_employees or 50,
                'num_machinery': len(extraction.machinery) if extraction.machinery else 3,
                'num_materials': len(extraction.materials) if extraction.materials else 5,
                'compliance_score': 1 if extraction.guidelines_followed else 0,
                'missing_docs_count': len(extraction.missing_documents) if extraction.missing_documents else 0
            }
            for key, value in features.items():
                print(f"  {key}: {value}")
            
            # Show risk scores
            print("\n5. Risk Scores:")
            for risk_type, score in risk_scores.items():
                print(f"  {risk_type}: {score:.4f}")
                
            # Show recommendations
            print("\n6. Recommendations:")
            for i, rec in enumerate(recommendations):
                print(f"  {i+1}. {rec.improvement_type} ({rec.priority}): {rec.description}")
                
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    debug_full_dpr_processing()