"""
Test script to demonstrate DPR chatbot prompt engineering
"""
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(backend_dir)

from app.ai.chatbot import DPRChatbot
from app.models.ai_models import EnhancedDPRExtraction, Recommendation, RiskLabel

def create_sample_dpr_data():
    """
    Create sample DPR data for testing
    """
    # Sample extraction data
    extraction = EnhancedDPRExtraction(
        project_title="Northeast Road Construction Project",
        department="Public Works Department",
        region="Northeast India",
        duration="24 months",
        estimated_cost="₹250 crore",
        fund_allocation="₹230 crore",
        contingency="₹20 crore",
        start_date="01/06/2024",
        end_date="01/06/2026",
        milestones=["Site Preparation", "Foundation Work", "Structural Construction", "Finishing", "Inspection"],
        num_employees=120,
        machinery=["Excavators", "Bulldozers", "Cranes", "Dump Trucks"],
        raw_materials=["Cement", "Steel", "Sand", "Bricks"],
        vendor_details=["ABC Construction Ltd", "XYZ Materials Corp"],
        state="Assam",
        district="Guwahati",
        coordinates="26.1433N, 91.6177E",
        risk_zone="Flood prone area",
        engineering_details="Standard road construction with reinforced concrete structures",
        specifications="IRC:21-2017 standards for rural road construction",
        materials=["Concrete", "Steel", "Asphalt"],
        guidelines_followed=True,
        missing_documents=["Environmental Clearance Certificate"],
        budget="₹250 crore",
        timeline="24 months",
        resource_allocation="120 employees",
        location="Guwahati, Assam",
        environmental_risks="Flood risk during monsoon season",
        technical_sections=["Introduction", "Methodology", "Implementation", "Conclusion"]
    )
    
    # Sample risk scores
    risk_scores = {
        "Cost Overrun": 0.65,
        "Schedule Delay": 0.45,
        "Resource Shortage": 0.30,
        "Environmental Risk": 0.75
    }
    
    # Sample recommendations
    recommendations = [
        Recommendation(
            improvement_type="Budget Rebalance",
            description="Increase contingency budget by 15% to account for flood-related delays",
            priority="High"
        ),
        Recommendation(
            improvement_type="Timeline Adjustment",
            description="Extend project timeline by 3 months to accommodate monsoon season",
            priority="High"
        ),
        Recommendation(
            improvement_type="Risk Mitigation",
            description="Implement flood mitigation measures including elevated construction and drainage systems",
            priority="High"
        ),
        Recommendation(
            improvement_type="Resource Planning",
            description="Establish alternative supply chains for raw materials during flood season",
            priority="Medium"
        )
    ]
    
    return extraction, risk_scores, recommendations

def test_chatbot_prompts():
    """
    Test various chatbot prompts with sample data
    """
    print("🧪 DPR Chatbot Prompt Engineering Test")
    print("=" * 50)
    
    # Create sample data
    extraction, risk_scores, recommendations = create_sample_dpr_data()
    
    # Initialize chatbot
    chatbot = DPRChatbot()
    
    # Create context
    context = chatbot.analyze_dpr(extraction, risk_scores, recommendations)
    
    # Test various prompts
    test_prompts = [
        "What is the biggest risk in this DPR?",
        "Can you provide a summary of the project?",
        "What recommendations do you have for improving this DPR?",
        "Is the budget allocation adequate for this project?",
        "What are the technical specifications?",
        "Are there any compliance issues?",
        "How does the location affect this project?",
        "What is the project timeline?",
        "Are there sufficient resources allocated?",
        "What reports can you generate?"
    ]
    
    print("\n📊 Testing Chatbot Responses:")
    print("-" * 30)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{i}. Question: {prompt}")
        response = chatbot.answer_question(prompt, context)
        print(f"   Response: {response[:200]}{'...' if len(response) > 200 else ''}")
    
    print("\n✅ Prompt engineering test completed successfully!")

def demonstrate_prompt_classification():
    """
    Demonstrate how the chatbot classifies different types of questions
    """
    print("\n🔍 Prompt Classification Demo")
    print("=" * 30)
    
    chatbot = DPRChatbot()
    
    test_questions = [
        "What is the biggest risk?",
        "How can we improve the budget?",
        "Give me a summary of the project",
        "Is the technical approach feasible?",
        "What is the estimated cost?",
        "Are we following all guidelines?",
        "How does the location affect the project?",
        "What are the key milestones?"
    ]
    
    for question in test_questions:
        question_type = chatbot._classify_question_type(question)
        print(f"Question: '{question}'")
        print(f"Classified as: {question_type}")
        print()

if __name__ == "__main__":
    print("🚀 Testing DPR Chatbot Prompt Engineering")
    
    try:
        test_chatbot_prompts()
        demonstrate_prompt_classification()
        
        print("\n🎯 Key Features Demonstrated:")
        print("  • Context-aware question answering")
        print("  • Intelligent prompt classification")
        print("  • Specialized response generation")
        print("  • Risk-based analysis")
        print("  • Recommendation provision")
        
        print("\n📝 For more examples, see CHATBOT_PROMPT_GUIDE.md")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        sys.exit(1)