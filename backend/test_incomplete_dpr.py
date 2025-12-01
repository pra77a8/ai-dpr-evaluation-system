"""
Test script to verify DPR extraction and risk calculation with incomplete information
"""
import os
import sys
from app.utils.dpr_processor import extract_dpr_elements
from app.services.risk_calculator import calculate_risk_scores

def test_incomplete_dpr():
    """Test DPR extraction and risk calculation with incomplete information"""
    
    # Test case 1: Complete DPR information
    complete_dpr_text = """
    Project Title: Rural Road Development - Phase 2
    
    Budget Details: ₹25,00,000 (Twenty-Five Lakhs)
    
    Timeline: 12 months (Jan 2025 - Dec 2025)
    
    Resources & Manpower: 50 laborers, 5 engineers, 10 vehicles
    
    Location / Region: Village Rampur to Highway NH-44, District East
    
    Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon
    """
    
    print("Test Case 1: Complete DPR Information")
    print("=" * 50)
    extracted_complete = extract_dpr_elements(complete_dpr_text)
    risk_complete = calculate_risk_scores(extracted_complete)
    
    print(f"Project Title: {extracted_complete.project_title}")
    print(f"Budget: {extracted_complete.budget}")
    print(f"Timeline: {extracted_complete.timeline}")
    print(f"Resources: {extracted_complete.resource_allocation}")
    print(f"Location: {extracted_complete.location}")
    print(f"Environmental: {extracted_complete.environmental_risks}")
    print()
    print("Risk Scores:")
    print(f"  Cost Overruns: {risk_complete.cost_overruns:.1f}")
    print(f"  Schedule Delays: {risk_complete.schedule_delays:.1f}")
    print(f"  Resource Shortages: {risk_complete.resource_shortages:.1f}")
    print(f"  Environmental Risks: {risk_complete.environmental_risks:.1f}")
    print()
    
    # Test case 2: Incomplete DPR information (missing budget and timeline)
    incomplete_dpr_text = """
    Project Title: Rural Road Development - Phase 2
    
    Location / Region: Village Rampur to Highway NH-44, District East
    
    Environmental Concerns: Minimal tree cutting required, flood-prone area during monsoon
    """
    
    print("Test Case 2: Incomplete DPR Information (Missing Budget & Timeline)")
    print("=" * 50)
    extracted_incomplete = extract_dpr_elements(incomplete_dpr_text)
    risk_incomplete = calculate_risk_scores(extracted_incomplete)
    
    print(f"Project Title: {extracted_incomplete.project_title}")
    print(f"Budget: {extracted_incomplete.budget}")
    print(f"Timeline: {extracted_incomplete.timeline}")
    print(f"Resources: {extracted_incomplete.resource_allocation}")
    print(f"Location: {extracted_incomplete.location}")
    print(f"Environmental: {extracted_incomplete.environmental_risks}")
    print()
    print("Risk Scores:")
    print(f"  Cost Overruns: {risk_incomplete.cost_overruns:.1f}")
    print(f"  Schedule Delays: {risk_incomplete.schedule_delays:.1f}")
    print(f"  Resource Shortages: {risk_incomplete.resource_shortages:.1f}")
    print(f"  Environmental Risks: {risk_incomplete.environmental_risks:.1f}")
    print()
    
    # Compare risks
    print("Risk Comparison:")
    print("=" * 50)
    print(f"Cost Overruns: {risk_complete.cost_overruns:.1f} → {risk_incomplete.cost_overruns:.1f} (+{risk_incomplete.cost_overruns - risk_complete.cost_overruns:.1f})")
    print(f"Schedule Delays: {risk_complete.schedule_delays:.1f} → {risk_incomplete.schedule_delays:.1f} (+{risk_incomplete.schedule_delays - risk_complete.schedule_delays:.1f})")
    print(f"Resource Shortages: {risk_complete.resource_shortages:.1f} → {risk_incomplete.resource_shortages:.1f} (+{risk_incomplete.resource_shortages - risk_complete.resource_shortages:.1f})")
    print(f"Environmental Risks: {risk_complete.environmental_risks:.1f} → {risk_incomplete.environmental_risks:.1f} (+{risk_incomplete.environmental_risks - risk_complete.environmental_risks:.1f})")
    
    # Test case 3: Large PDF with scattered information
    large_pdf_text = """
    ANNUAL REPORT 2025
    ==================
    
    Page 1: Table of Contents
    Page 2-5: Executive Summary
    Page 6-10: Financial Overview
    
    PROJECT DETAILS
    ===============
    
    Project Title: Rural Road Development - Phase 2
    This project aims to develop rural road infrastructure...
    
    Page 11-15: Technical Specifications
    Page 16-20: Environmental Impact Assessment
    
    BUDGET ALLOCATION
    =================
    The total budget for this project is ₹25,00,000...
    
    Page 21-25: Timeline and Milestones
    Page 26-30: Resource Allocation
    
    RESOURCES
    =========
    The project will require:
    - 50 laborers
    - 5 engineers
    - 10 vehicles
    
    Page 31-35: Risk Assessment
    Page 36-40: Conclusion and Recommendations
    
    ENVIRONMENTAL CONCERNS
    ======================
    The project area is flood-prone during monsoon season...
    Minimal tree cutting will be required...
    """
    
    print()
    print("Test Case 3: Large PDF with Scattered Information")
    print("=" * 50)
    extracted_large = extract_dpr_elements(large_pdf_text)
    risk_large = calculate_risk_scores(extracted_large)
    
    print(f"Project Title: {extracted_large.project_title}")
    print(f"Budget: {extracted_large.budget}")
    print(f"Timeline: {extracted_large.timeline}")
    print(f"Resources: {extracted_large.resource_allocation}")
    print(f"Location: {extracted_large.location}")
    print(f"Environmental: {extracted_large.environmental_risks}")
    print()
    print("Risk Scores:")
    print(f"  Cost Overruns: {risk_large.cost_overruns:.1f}")
    print(f"  Schedule Delays: {risk_large.schedule_delays:.1f}")
    print(f"  Resource Shortages: {risk_large.resource_shortages:.1f}")
    print(f"  Environmental Risks: {risk_large.environmental_risks:.1f}")

if __name__ == "__main__":
    test_incomplete_dpr()