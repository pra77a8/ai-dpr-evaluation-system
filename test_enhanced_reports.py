"""
Test script to verify enhanced report generation with unique content for each PDF
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.ai.ai_service import AIService
from backend.app.models.ai_models import EnhancedDPRExtraction

def test_enhanced_report_generation():
    """Test that reports are generated with unique content based on DPR data"""
    
    print("=== Testing Enhanced Report Generation ===")
    
    # Initialize AI service
    ai_service = AIService()
    
    # Test DPR 1 - Road construction project
    print("\n1. Testing Road Construction Project...")
    extraction1 = EnhancedDPRExtraction(
        project_title="Road Construction Project in Assam",
        department="Public Works Department",
        state="Assam",
        district="Guwahati",
        duration="18 months",
        estimated_cost="₹150 crore",
        num_employees=150,
        environmental_risks="Flood prone area",
        risk_zone="High flood risk zone"
    )
    
    risk_scores1 = {
        "cost_overruns": 0.75,
        "schedule_delays": 0.65,
        "resource_shortages": 0.55,
        "environmental_risks": 0.85
    }
    
    recommendations1 = ai_service.generate_recommendations(risk_scores1, 85.0)
    
    # Generate reports
    analytical_report1 = ai_service.generate_analytical_report(
        "test_dpr_1", extraction1, risk_scores1, recommendations1
    )
    
    recommendation_report1 = ai_service.generate_recommendation_report(
        "test_dpr_1", extraction1, risk_scores1, recommendations1
    )
    
    print(f"   Analytical Report 1: {analytical_report1}")
    print(f"   Recommendation Report 1: {recommendation_report1}")
    
    # Test DPR 2 - School building project
    print("\n2. Testing School Building Project...")
    extraction2 = EnhancedDPRExtraction(
        project_title="School Building Project in Rajasthan",
        department="Education Department",
        state="Rajasthan",
        district="Jaipur",
        duration="24 months",
        estimated_cost="₹75 crore",
        num_employees=80,
        environmental_risks="Desert conditions",
        risk_zone="High temperature zone"
    )
    
    risk_scores2 = {
        "cost_overruns": 0.45,
        "schedule_delays": 0.55,
        "resource_shortages": 0.35,
        "environmental_risks": 0.65
    }
    
    recommendations2 = ai_service.generate_recommendations(risk_scores2, 70.0)
    
    # Generate reports
    analytical_report2 = ai_service.generate_analytical_report(
        "test_dpr_2", extraction2, risk_scores2, recommendations2
    )
    
    recommendation_report2 = ai_service.generate_recommendation_report(
        "test_dpr_2", extraction2, risk_scores2, recommendations2
    )
    
    print(f"   Analytical Report 2: {analytical_report2}")
    print(f"   Recommendation Report 2: {recommendation_report2}")
    
    # Verify that reports are different
    print("\n3. Verifying Report Uniqueness...")
    if analytical_report1 != analytical_report2:
        print("   ✅ Analytical reports are unique")
    else:
        print("   ❌ Analytical reports are identical")
        
    if recommendation_report1 != recommendation_report2:
        print("   ✅ Recommendation reports are unique")
    else:
        print("   ❌ Recommendation reports are identical")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_enhanced_report_generation()