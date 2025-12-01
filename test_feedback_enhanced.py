"""
Test script for the enhanced feedback functionality
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Mock the database functions for testing
class MockCollection:
    def __init__(self):
        self.data = {}
        self.counter = 1
    
    def find_one(self, query):
        # Simple mock implementation
        for item in self.data.values():
            match = True
            for key, value in query.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                return item
        return None
    
    def find(self, query=None):
        # Simple mock implementation
        if query is None:
            return list(self.data.values())
        
        results = []
        for item in self.data.values():
            match = True
            for key, value in query.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                results.append(item)
        return results
    
    def insert_one(self, doc):
        doc_id = str(self.counter)
        self.counter += 1
        doc["_id"] = doc_id
        self.data[doc_id] = doc
        class Result:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return Result(doc_id)
    
    def update_one(self, query, update):
        # Simple mock implementation
        for item in self.data.values():
            match = True
            for key, value in query.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                # Apply update
                set_data = update.get("$set", {})
                for key, value in set_data.items():
                    item[key] = value
                break

# Mock the database collections
mock_feedbacks_collection = MockCollection()
mock_users_collection = MockCollection()
mock_dprs_collection = MockCollection()

# Populate with sample data
mock_users_collection.insert_one({
    "_id": "user1",
    "name": "John Civilian",
    "email": "john@example.com",
    "role": "Civilian"
})

mock_users_collection.insert_one({
    "_id": "user2",
    "name": "Jane Organization",
    "email": "jane@example.com",
    "role": "Organization"
})

mock_dprs_collection.insert_one({
    "_id": "dpr1",
    "file_name": "sample_dpr.pdf",
    "project_title": "Road Construction Project"
})

def get_feedbacks_collection():
    return mock_feedbacks_collection

def get_users_collection():
    return mock_users_collection

def get_dprs_collection():
    return mock_dprs_collection

# Replace the database functions with mocks
import app.database
app.database.get_feedbacks_collection = get_feedbacks_collection
app.database.get_users_collection = get_users_collection
app.database.get_dprs_collection = get_dprs_collection

# Import the feedback routes for testing
from app.routes.feedback import (
    submit_feedback,
    get_feedbacks_by_project,
    get_feedbacks_by_user,
    like_feedback,
    dislike_feedback,
    get_all_feedbacks_for_organization,
    get_feedback
)

from app.models.feedback import FeedbackCreate

async def test_feedback_functionality():
    """Test the enhanced feedback functionality"""
    
    print("=== Testing Enhanced Feedback Functionality ===\n")
    
    # Test 1: Submit feedback
    print("1. Submitting feedback...")
    feedback_create = FeedbackCreate(
        dpr_id="dpr1",
        project_title="Road Construction Project",
        civilian_id="user1",
        content="This project will greatly benefit our community. I hope it gets approved soon!"
    )
    
    try:
        feedback_response = await submit_feedback(feedback_create)
        feedback_id = feedback_response["id"]
        print(f"   Feedback submitted successfully with ID: {feedback_id}")
        print(f"   Content: {feedback_response['content']}")
        print(f"   Submitted by: {feedback_response['civilian_name']}")
        print(f"   Likes: {feedback_response['likes_count']}, Dislikes: {feedback_response['dislikes_count']}")
    except Exception as e:
        print(f"   Error submitting feedback: {e}")
        return
    
    print()
    
    # Test 2: Get feedback by project
    print("2. Getting feedbacks by project...")
    try:
        project_feedbacks = await get_feedbacks_by_project("dpr1")
        print(f"   Found {len(project_feedbacks)} feedback(s) for the project")
        for feedback in project_feedbacks:
            print(f"   - {feedback['civilian_name']}: {feedback['content']}")
            print(f"     Likes: {feedback['likes_count']}, Dislikes: {feedback['dislikes_count']}")
    except Exception as e:
        print(f"   Error getting feedbacks by project: {e}")
    
    print()
    
    # Test 3: Get feedback by user
    print("3. Getting feedbacks by user...")
    try:
        user_feedbacks = await get_feedbacks_by_user("user1")
        print(f"   Found {len(user_feedbacks)} feedback(s) by the user")
        for feedback in user_feedbacks:
            print(f"   - {feedback['project_title']}: {feedback['content']}")
            print(f"     Likes: {feedback['likes_count']}, Dislikes: {feedback['dislikes_count']}")
    except Exception as e:
        print(f"   Error getting feedbacks by user: {e}")
    
    print()
    
    # Test 4: Like feedback
    print("4. Liking feedback...")
    try:
        liked_feedback = await like_feedback(feedback_id, "user2")
        print(f"   Feedback liked successfully")
        print(f"   Likes: {liked_feedback['likes_count']}, Dislikes: {liked_feedback['dislikes_count']}")
    except Exception as e:
        print(f"   Error liking feedback: {e}")
    
    print()
    
    # Test 5: Dislike feedback
    print("5. Disliking feedback...")
    try:
        disliked_feedback = await dislike_feedback(feedback_id, "user2")
        print(f"   Feedback disliked successfully")
        print(f"   Likes: {disliked_feedback['likes_count']}, Dislikes: {disliked_feedback['dislikes_count']}")
    except Exception as e:
        print(f"   Error disliking feedback: {e}")
    
    print()
    
    # Test 6: Get all feedbacks for organization dashboard
    print("6. Getting all feedbacks for organization dashboard...")
    try:
        all_feedbacks = await get_all_feedbacks_for_organization()
        print(f"   Found {len(all_feedbacks)} feedback(s) in total")
        for feedback in all_feedbacks:
            print(f"   - {feedback['civilian_name']}: {feedback['content']}")
            print(f"     Likes: {feedback['likes_count']}, Dislikes: {feedback['dislikes_count']}")
    except Exception as e:
        print(f"   Error getting all feedbacks: {e}")
    
    print()
    
    # Test 7: Get specific feedback
    print("7. Getting specific feedback...")
    try:
        specific_feedback = await get_feedback(feedback_id)
        print(f"   Feedback found:")
        print(f"   - {specific_feedback['civilian_name']}: {specific_feedback['content']}")
        print(f"     Likes: {specific_feedback['likes_count']}, Dislikes: {specific_feedback['dislikes_count']}")
    except Exception as e:
        print(f"   Error getting specific feedback: {e}")
    
    print("\n=== Testing Complete ===")

if __name__ == "__main__":
    asyncio.run(test_feedback_functionality())