import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.database import get_users_collection, get_feedbacks_collection
import json
from bson import ObjectId

def check_users_and_feedback():
    """Check users and feedback in the database"""
    
    print("=== USERS AND FEEDBACK ANALYSIS ===")
    print()
    
    # Check users collection
    users_collection = get_users_collection()
    users = list(users_collection.find())
    
    print(f"Found {len(users)} users:")
    print("-" * 40)
    
    for user in users:
        print(f"User ID: {user.get('_id', 'N/A')}")
        print(f"  Name: {user.get('name', 'N/A')}")
        print(f"  Email: {user.get('email', 'N/A')}")
        print(f"  Role: {user.get('role', 'N/A')}")
        print()
    
    # Check feedbacks collection
    feedbacks_collection = get_feedbacks_collection()
    feedbacks = list(feedbacks_collection.find())
    
    print(f"Found {len(feedbacks)} feedbacks:")
    print("-" * 40)
    
    for feedback in feedbacks:
        print(f"Feedback ID: {feedback.get('_id', 'N/A')}")
        print(f"  DPR ID: {feedback.get('dpr_id', 'N/A')}")
        print(f"  Project Title: {feedback.get('project_title', 'N/A')}")
        print(f"  Civilian ID: {feedback.get('civilian_id', 'N/A')}")
        print(f"  Civilian Name: {feedback.get('civilian_name', 'N/A')}")
        print(f"  Content: {feedback.get('content', 'N/A')}")
        print(f"  Likes: {feedback.get('likes', [])}")
        print(f"  Dislikes: {feedback.get('dislikes', [])}")
        print(f"  Submitted At: {feedback.get('submitted_at', 'N/A')}")
        print()
    
    print("=== ANALYSIS COMPLETE ===")

if __name__ == "__main__":
    check_users_and_feedback()