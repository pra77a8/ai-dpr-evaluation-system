"""
Simple test script for the DPR chatbot
"""
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.join(os.path.dirname(__file__), '.')
sys.path.append(backend_dir)

def test_chatbot():
    """
    Test the DPR chatbot functionality
    """
    print("Testing DPR Chatbot...")
    
    # Import the chatbot
    try:
        from app.ai.chatbot import DPRChatbot
        print("✅ Chatbot imported successfully")
    except Exception as e:
        print(f"❌ Failed to import chatbot: {e}")
        return
    
    # Import the prompt system
    try:
        from app.ai.chatbot_prompts import DPRChatbotPrompts
        print("✅ Prompt system imported successfully")
    except Exception as e:
        print(f"❌ Failed to import prompt system: {e}")
        return
    
    # Test prompt classification
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
    
    print("\nTesting prompt classification:")
    for question in test_questions:
        question_type = chatbot._classify_question_type(question)
        print(f"  '{question}' -> {question_type}")
    
    print("\n✅ Chatbot test completed successfully!")

if __name__ == "__main__":
    test_chatbot()