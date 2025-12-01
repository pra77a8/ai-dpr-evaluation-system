"""
Simple test for generic DPR extraction
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.ai.nlp_extractor import NLPExtractor

# Sample text from the PDF that we know contains the project title
sample_text = """
DETAILED PROJECT REPORT (DPR)
For
Roll-Out of National e-Vidhan Application(NeVA)
(Development of Mobile Application & AI enabled Transcription & Translation Services)

Ministry of Parliamentary Affairs
Government of India

April, 2023

1. EXECUTIVE SUMMARY

The National e-Vidhan Application (NeVA) is a Mission Mode Project (MMP) under the Digital India Programme. The project aims at bringing all the legislatures of the country together on one platform, thereby improving the efficiency and transparency of the legislative processes. The project involves digitization of various activities of the State Legislatures/Assemblies, including the development of Mobile Applications, AI enabled Transcription and Translation Services, etc.

2. PROJECT OBJECTIVES

The main objectives of the project are:
• To develop a Mobile Application for the Legislators, Officers and other stakeholders
• To implement AI enabled Transcription Services for automatic transcription of the proceedings
• To implement AI enabled Translation Services for translation of the proceedings in regional languages
• To enhance the existing NeVA platform with new features and functionalities

3. SCOPE OF WORK

The scope of work includes:
• Development of Mobile Application for Android and iOS platforms
• Implementation of AI enabled Transcription Services using Automatic Speech Recognition (ASR) technology
• Implementation of AI enabled Translation Services using Neural Machine Translation (NMT) technology
• Integration of the new services with the existing NeVA platform
• Testing and deployment of the complete solution

4. TECHNICAL SPECIFICATIONS

The technical specifications of the project are as follows:
• Mobile Application: Native applications for Android and iOS platforms
• Transcription Services: Cloud based ASR engine with domain specific language models
• Translation Services: Neural Machine Translation engine with custom language models
• Platform Integration: RESTful APIs for integration with NeVA platform
• Security: End-to-end encryption and secure authentication mechanisms

5. PROJECT TIMELINE

The project will be executed in the following phases:
• Phase 1: Requirements gathering and design (2 months)
• Phase 2: Development of Mobile Application (4 months)
• Phase 3: Implementation of AI services (6 months)
• Phase 4: Integration and testing (3 months)
• Phase 5: Deployment and training (1 month)

Total project duration: 16 months

6. BUDGET ESTIMATES

The budget estimates for the project are as follows:
• Mobile Application Development: ₹15.00 Crore
• AI Services Implementation: ₹25.00 Crore
• Platform Integration: ₹5.00 Crore
• Testing and Deployment: ₹3.00 Crore
• Training and Support: ₹2.00 Crore

Total estimated cost: ₹50.00 Crore

7. RESOURCE REQUIREMENTS

The project requires the following resources:
• Project Manager: 1
• Technical Architects: 2
• Mobile Application Developers: 6
• AI Engineers: 8
• Integration Specialists: 3
• QA Engineers: 4
• Technical Writers: 2

Total team size: 26

8. RISK ANALYSIS

The major risks identified for the project are:
• Technology risks related to accuracy of ASR and NMT engines
• Integration risks with the existing NeVA platform
• Data security and privacy risks
• Resource availability risks

Mitigation measures:
• Conducting Proof of Concept (PoC) for ASR and NMT technologies
• Following standard integration practices and protocols
• Implementing robust security measures and compliance checks
• Maintaining a resource buffer and backup plans

9. APPROVAL MATRIX

The project requires approvals from the following authorities:
• Ministry of Parliamentary Affairs
• Digital India Programme Office
• Expenditure Finance Committee (EFC), if applicable

10. CONCLUSION

The Roll-Out of National e-Vidhan Application (NeVA) project is a strategic initiative that will significantly enhance the legislative processes in the country. The project leverages modern technologies like AI and Mobile platforms to improve efficiency, transparency and accessibility of legislative proceedings. With proper planning, execution and monitoring, the project is expected to deliver significant benefits to all stakeholders.
"""

def test_generic_extraction():
    """Test the generic extraction with sample text"""
    print("=== Testing Generic DPR Extraction ===")
    
    try:
        # Initialize the generic NLP extractor
        extractor = NLPExtractor()
        
        # Extract entities using the generic approach
        extraction = extractor.extract_entities(sample_text)
        
        # Print results
        print("\n=== Extraction Results ===")
        print(f"Project Title: {extraction.project_title}")
        print(f"Department: {extraction.department}")
        print(f"Estimated Cost: {extraction.estimated_cost}")
        print(f"Duration: {extraction.duration}")
        print(f"Region: {extraction.region}")
        print(f"State: {extraction.state}")
        print(f"District: {extraction.district}")
        print(f"Risk Zone: {extraction.risk_zone}")
        print(f"Number of Employees: {extraction.num_employees}")
        print(f"Milestones: {extraction.milestones}")
        print(f"Machinery: {extraction.machinery}")
        print(f"Materials: {extraction.materials}")
        print(f"Vendor Details: {extraction.vendor_details}")
        print(f"Guidelines Followed: {extraction.guidelines_followed}")
        print(f"Missing Documents: {extraction.missing_documents}")
            
        print("\n=== Test completed successfully ===")
        
        # Check if we successfully extracted the project title
        if extraction.project_title and "Roll-Out of National e-Vidhan Application" in extraction.project_title:
            print("\n✅ SUCCESS: Project title correctly extracted!")
        else:
            print("\n❌ FAILURE: Project title not correctly extracted")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generic_extraction()