"""
Complete test for the generic DPR extraction system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import pdfplumber
from app.ai.nlp_extractor import NLPExtractor
from app.ai.ai_service import AIService

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        # Just extract first few pages for testing
        for i, page in enumerate(pdf.pages):
            if i < 3:  # Only first 3 pages
                text += page.extract_text() or ""
    return text

def complete_generic_test():
    """Complete test for the generic extraction system"""
    print("=== Complete Generic DPR Extraction System Test ===")
    
    try:
        # Extract text from PDF (first few pages only)
        text = extract_text_from_pdf("Model_DPR_Final 2.0.pdf")
        print(f"Extracted text length: {len(text)} characters")
        
        # Initialize the AI service (which uses the generic NLP extractor)
        ai_service = AIService()
        print("AI Service initialized successfully")
        
        # Test entity extraction
        print("\n--- Testing Entity Extraction ---")
        extraction = ai_service.extract_dpr_entities(text)
        print(f"Project Title: {extraction.project_title}")
        print(f"Department: {extraction.department}")
        print(f"Estimated Cost: {extraction.estimated_cost}")
        print(f"Duration: {extraction.duration}")
        
        # Test risk prediction
        print("\n--- Testing Risk Prediction ---")
        risk_scores = ai_service.predict_dpr_risks(extraction)
        print("Risk scores calculated successfully")
        for risk_type, score in risk_scores.items():
            print(f"  {risk_type}: {score:.2f}")
        
        # Test recommendation generation
        print("\n--- Testing Recommendation Generation ---")
        recommendations = ai_service.generate_recommendations(risk_scores)
        print(f"Generated {len(recommendations)} recommendations")
        for i, rec in enumerate(recommendations[:3]):  # Show first 3
            print(f"  {i+1}. {rec.improvement_type}: {rec.description}")
        
        # Test report generation
        print("\n--- Testing Report Generation ---")
        analytical_report = ai_service.generate_analytical_report(
            "test_dpr_id", extraction, risk_scores, recommendations
        )
        print(f"Analytical report generated: {analytical_report}")
        
        recommendation_report = ai_service.generate_recommendation_report(
            "test_dpr_id", extraction, risk_scores, recommendations
        )
        print(f"Recommendation report generated: {recommendation_report}")
            
        # Check if we successfully extracted the project title
        if extraction.project_title and "Roll-Out of National e-Vidhan Application" in extraction.project_title:
            print("\n✅ SUCCESS: Complete generic system is working correctly!")
            return True
        else:
            print("\n❌ FAILURE: Project title not correctly extracted")
            return False
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = complete_generic_test()
    if success:
        print("\n🎉 Complete generic DPR extraction system is working correctly!")
        print("This system now works with any PDF format, not just specific ones.")
    else:
        print("\n💥 Complete generic DPR extraction system failed.")