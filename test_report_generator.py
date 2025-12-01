import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app.ai.report_generator import ReportGenerator
    from app.models.ai_models import EnhancedDPRExtraction, Recommendation
    print("✓ Report generator imported successfully")
    
    # Create a simple extraction
    extraction = EnhancedDPRExtraction(
        project_title="Test Project",
        department="Test Department",
        estimated_cost="₹100 crore",
        duration="12 months"
    )
    
    # Create simple risk scores
    risk_scores = {
        "cost_overruns": 0.5,
        "schedule_delays": 0.3,
        "resource_shortages": 0.2,
        "environmental_risks": 0.1
    }
    
    # Create simple recommendations
    recommendations = [
        Recommendation(
            improvement_type="Test Recommendation",
            description="This is a test recommendation",
            priority="Medium"
        )
    ]
    
    # Test report generation
    report_generator = ReportGenerator()
    analytical_report = report_generator.generate_analytical_report(
        "test_dpr", extraction, risk_scores, recommendations
    )
    print(f"✓ Analytical report generated: {analytical_report}")
    
    recommendation_report = report_generator.generate_recommendation_report(
        "test_dpr", extraction, risk_scores, recommendations
    )
    print(f"✓ Recommendation report generated: {recommendation_report}")
    
    # Clean up
    if os.path.exists(analytical_report):
        os.remove(analytical_report)
        print("✓ Analytical report cleaned up")
        
    if os.path.exists(recommendation_report):
        os.remove(recommendation_report)
        print("✓ Recommendation report cleaned up")
        
except Exception as e:
    print(f"✗ Error with report generation: {e}")
    import traceback
    traceback.print_exc()