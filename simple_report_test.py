"""
Simple test to verify report generation enhancements
"""

# Test the enhanced report generator directly
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the report generator
from backend.app.ai.report_generator import ReportGenerator
from backend.app.models.ai_models import EnhancedDPRExtraction, Recommendation

def test_report_generator():
    """Test the enhanced report generator"""
    
    print("=== Testing Enhanced Report Generator ===")
    
    # Create report generator
    report_gen = ReportGenerator()
    
    # Create test extraction data
    extraction = EnhancedDPRExtraction(
        project_title="Road Construction Project",
        department="Public Works Department",
        state="Assam",
        district="Guwahati",
        duration="18 months",
        estimated_cost="₹150 crore",
        num_employees=150,
        environmental_risks="Flood prone area",
        risk_zone="High flood risk zone"
    )
    
    # Create test risk scores
    risk_scores = {
        "cost_overruns": 0.75,
        "schedule_delays": 0.65,
        "resource_shortages": 0.55,
        "environmental_risks": 0.85
    }
    
    # Create test recommendations
    recommendations = [
        Recommendation(
            improvement_type="Budget Rebalance",
            description="Increase contingency budget by 10-15%",
            priority="High"
        ),
        Recommendation(
            improvement_type="Timeline Adjustment",
            description="Timeline too short — extend by 3-6 months",
            priority="High"
        )
    ]
    
    # Generate analytical report
    print("\n1. Generating Analytical Report...")
    analytical_report = report_gen.generate_analytical_report(
        "test_dpr_1", extraction, risk_scores, recommendations
    )
    print(f"   Generated: {analytical_report}")
    
    # Generate recommendation report
    print("\n2. Generating Recommendation Report...")
    recommendation_report = report_gen.generate_recommendation_report(
        "test_dpr_1", extraction, risk_scores, recommendations
    )
    print(f"   Generated: {recommendation_report}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_report_generator()