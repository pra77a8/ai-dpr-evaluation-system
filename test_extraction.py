#!/usr/bin/env python3
"""
Test script to verify DPR data extraction functionality
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.ai.ai_service import AIService
from backend.app.ai.nlp_extractor import NLPExtractor

def test_extraction():
    # Sample DPR text for testing
    sample_text = """
    PROJECT TITLE: Road Construction and Community Development Project
    
    BUDGET: 
    Total Project Cost: ₹150 crore
    Fund Allocation: ₹140 crore
    Contingency: ₹10 crore
    
    DURATION: 18 months
    
    LOCATION: 
    State: Assam
    District: Guwahati
    
    RESOURCES & MANPOWER:
    Number of employees: 150
    Machinery: Excavators, Bulldozers, Trucks
    
    ENGINEERING DETAILS:
    Standard road construction specifications following government guidelines
    
    GUIDELINES FOLLOWED: Yes
    
    RISK ZONE: Flood prone area
    """

    print("Testing DPR data extraction...")
    print("=" * 50)
    
    # Initialize AI service
    ai_service = AIService()
    
    # Extract entities
    print("Extracting entities...")
    extraction = ai_service.extract_dpr_entities(sample_text)
    
    # Print results
    print("\nExtracted Data:")
    print("-" * 30)
    print(f"Project Title: {extraction.project_title}")
    print(f"Department: {extraction.department}")
    print(f"Estimated Cost: {extraction.estimated_cost}")
    print(f"Duration: {extraction.duration}")
    print(f"State: {extraction.state}")
    print(f"District: {extraction.district}")
    print(f"Number of Employees: {extraction.num_employees}")
    print(f"Risk Zone: {extraction.risk_zone}")
    print(f"Guidelines Followed: {extraction.guidelines_followed}")
    
    # Calculate completeness
    completeness = ai_service.calculate_completeness_score(extraction)
    print(f"\nCompleteness Score: {completeness:.2f}%")
    
    # Predict risks
    print("\nPredicting risks...")
    risk_scores = ai_service.predict_dpr_risks(extraction)
    print("Risk Scores:")
    for risk_type, score in risk_scores.items():
        print(f"  {risk_type}: {score:.2f}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_extraction()