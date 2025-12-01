import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.ai.ai_service import AIService
from app.models.ai_models import EnhancedDPRExtraction

def test_ai_service():
    """
    Test the AI service with a sample DPR text
    """
    # Initialize AI service
    ai_service = AIService()
    
    # Sample DPR text for testing
    sample_text = """
    DETAILED PROJECT REPORT (DPR)
    For
    Rural Road Development - Phase 2
    In
    Assam
    
    Project Title: Rural Road Development - Phase 2
    Department: Public Works Department
    State: Assam
    District: East District
    Duration: 24 months
    Estimated Cost: ₹30,00,000
    Fund Allocation: ₹25,00,000
    Contingency: ₹5,00,000
    Start Date: 01/01/2024
    End Date: 31/12/2025
    Number of Employees: 50
    Risk Zone: Flood prone area
    Engineering Details: Standard road construction specifications
    Guidelines Followed: Yes
    Milestones: Site Preparation, Foundation Work, Construction, Finishing
    Machinery: Excavators, Bulldozers, Cranes
    Materials: Cement, Steel, Sand
    """
    
    print("Testing AI Service...")
    print("=" * 50)
    
    # Test entity extraction
    print("1. Testing entity extraction...")
    extraction = ai_service.extract_dpr_entities(sample_text)
    print(f"Project Title: {extraction.project_title}")
    print(f"Department: {extraction.department}")
    print(f"Estimated Cost: {extraction.estimated_cost}")
    print(f"Duration: {extraction.duration}")
    print(f"State: {extraction.state}")
    print(f"District: {extraction.district}")
    print()
    
    # Test risk prediction
    print("2. Testing risk prediction...")
    risk_scores = ai_service.predict_dpr_risks(extraction)
    for risk_type, score in risk_scores.items():
        print(f"{risk_type}: {score:.2f}")
    print()
    
    # Test completeness score
    print("3. Testing completeness score...")
    completeness_score = ai_service.calculate_completeness_score(extraction)
    print(f"Completeness Score: {completeness_score:.2f}%")
    print()
    
    # Test recommendations
    print("4. Testing recommendations...")
    recommendations = ai_service.generate_recommendations(risk_scores, completeness_score)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec.description} (Priority: {rec.priority})")
    print()
    
    # Test chatbot
    print("5. Testing chatbot...")
    question = "What is the biggest risk in this DPR?"
    answer = ai_service.answer_dpr_question(question, extraction, risk_scores, recommendations)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print()
    
    print("AI Service test completed successfully!")

if __name__ == "__main__":
    test_ai_service()