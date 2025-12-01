from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
from app.models.feedback import FeedbackCreate, FeedbackResponse
from app.database import get_feedbacks_collection, get_dprs_collection, get_users_collection

router = APIRouter()

@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackCreate):
    feedbacks_collection = get_feedbacks_collection()
    dprs_collection = get_dprs_collection()
    users_collection = get_users_collection()
    
    # Verify DPR exists
    dpr = dprs_collection.find_one({"_id": ObjectId(feedback.dpr_id)})
    if not dpr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DPR not found"
        )
    
    # Get civilian name
    civilian = users_collection.find_one({"_id": ObjectId(feedback.civilian_id)})
    civilian_name = civilian["name"] if civilian else "Unknown User"
    
    # Create feedback document
    feedback_doc = {
        "dpr_id": feedback.dpr_id,
        "project_title": feedback.project_title,
        "civilian_id": feedback.civilian_id,
        "civilian_name": civilian_name,
        "content": feedback.content,
        "submitted_at": datetime.utcnow(),
        "likes": [],
        "dislikes": []
    }
    
    # Insert feedback into database
    result = feedbacks_collection.insert_one(feedback_doc)
    feedback_doc["id"] = str(result.inserted_id)
    
    # Add computed fields for response
    feedback_doc["likes_count"] = len(feedback_doc["likes"])
    feedback_doc["dislikes_count"] = len(feedback_doc["dislikes"])
    
    return feedback_doc

@router.get("/project/{dpr_id}", response_model=List[FeedbackResponse])
async def get_feedbacks_by_project(dpr_id: str):
    feedbacks_collection = get_feedbacks_collection()
    users_collection = get_users_collection()
    
    # Find all feedbacks for a specific project
    feedbacks = list(feedbacks_collection.find({"dpr_id": dpr_id}))
    
    # Format response
    for feedback in feedbacks:
        feedback["id"] = str(feedback["_id"])
        del feedback["_id"]
        # Add computed fields
        feedback["likes_count"] = len(feedback.get("likes", []))
        feedback["dislikes_count"] = len(feedback.get("dislikes", []))
        # Ensure civilian_name is present
        if "civilian_name" not in feedback:
            civilian = users_collection.find_one({"_id": ObjectId(feedback["civilian_id"])})
            feedback["civilian_name"] = civilian["name"] if civilian else "Unknown User"
    
    return feedbacks

@router.get("/user/{civilian_id}", response_model=List[FeedbackResponse])
async def get_feedbacks_by_user(civilian_id: str):
    feedbacks_collection = get_feedbacks_collection()
    users_collection = get_users_collection()
    
    # Find all feedbacks submitted by a specific user
    feedbacks = list(feedbacks_collection.find({"civilian_id": civilian_id}))
    
    # Format response
    for feedback in feedbacks:
        feedback["id"] = str(feedback["_id"])
        del feedback["_id"]
        # Add computed fields
        feedback["likes_count"] = len(feedback.get("likes", []))
        feedback["dislikes_count"] = len(feedback.get("dislikes", []))
        # Ensure civilian_name is present
        if "civilian_name" not in feedback:
            civilian = users_collection.find_one({"_id": ObjectId(feedback["civilian_id"])})
            feedback["civilian_name"] = civilian["name"] if civilian else "Unknown User"
    
    return feedbacks

@router.post("/{feedback_id}/like", response_model=FeedbackResponse)
async def like_feedback(feedback_id: str, user_id: str):
    feedbacks_collection = get_feedbacks_collection()
    users_collection = get_users_collection()
    
    # Find the feedback
    feedback = feedbacks_collection.find_one({"_id": ObjectId(feedback_id)})
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Initialize likes/dislikes if they don't exist
    if "likes" not in feedback:
        feedback["likes"] = []
    if "dislikes" not in feedback:
        feedback["dislikes"] = []
    
    # Remove user from dislikes if they previously disliked
    if user_id in feedback["dislikes"]:
        feedback["dislikes"].remove(user_id)
    
    # Add user to likes if not already there
    if user_id not in feedback["likes"]:
        feedback["likes"].append(user_id)
    
    # Update the feedback
    feedbacks_collection.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": {"likes": feedback["likes"], "dislikes": feedback["dislikes"]}}
    )
    
    # Format response
    feedback["id"] = str(feedback["_id"])
    del feedback["_id"]
    # Add computed fields
    feedback["likes_count"] = len(feedback.get("likes", []))
    feedback["dislikes_count"] = len(feedback.get("dislikes", []))
    # Ensure civilian_name is present
    if "civilian_name" not in feedback:
        civilian = users_collection.find_one({"_id": ObjectId(feedback["civilian_id"])})
        feedback["civilian_name"] = civilian["name"] if civilian else "Unknown User"
    
    return feedback

@router.post("/{feedback_id}/dislike", response_model=FeedbackResponse)
async def dislike_feedback(feedback_id: str, user_id: str):
    feedbacks_collection = get_feedbacks_collection()
    users_collection = get_users_collection()
    
    # Find the feedback
    feedback = feedbacks_collection.find_one({"_id": ObjectId(feedback_id)})
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Initialize likes/dislikes if they don't exist
    if "likes" not in feedback:
        feedback["likes"] = []
    if "dislikes" not in feedback:
        feedback["dislikes"] = []
    
    # Remove user from likes if they previously liked
    if user_id in feedback["likes"]:
        feedback["likes"].remove(user_id)
    
    # Add user to dislikes if not already there
    if user_id not in feedback["dislikes"]:
        feedback["dislikes"].append(user_id)
    
    # Update the feedback
    feedbacks_collection.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": {"likes": feedback["likes"], "dislikes": feedback["dislikes"]}}
    )
    
    # Format response
    feedback["id"] = str(feedback["_id"])
    del feedback["_id"]
    # Add computed fields
    feedback["likes_count"] = len(feedback.get("likes", []))
    feedback["dislikes_count"] = len(feedback.get("dislikes", []))
    # Ensure civilian_name is present
    if "civilian_name" not in feedback:
        civilian = users_collection.find_one({"_id": ObjectId(feedback["civilian_id"])})
        feedback["civilian_name"] = civilian["name"] if civilian else "Unknown User"
    
    return feedback

@router.get("/organization/dashboard", response_model=List[FeedbackResponse])
async def get_all_feedbacks_for_organization():
    """
    Get all feedbacks for organization dashboard with like/dislike counts
    """
    feedbacks_collection = get_feedbacks_collection()
    users_collection = get_users_collection()
    
    # Find all feedbacks
    feedbacks = list(feedbacks_collection.find({}))
    
    # Format response
    for feedback in feedbacks:
        feedback["id"] = str(feedback["_id"])
        del feedback["_id"]
        # Add computed fields
        feedback["likes_count"] = len(feedback.get("likes", []))
        feedback["dislikes_count"] = len(feedback.get("dislikes", []))
        # Ensure civilian_name is present
        if "civilian_name" not in feedback:
            civilian = users_collection.find_one({"_id": ObjectId(feedback["civilian_id"])})
            feedback["civilian_name"] = civilian["name"] if civilian else "Unknown User"
    
    # Sort by submitted date (newest first)
    feedbacks.sort(key=lambda x: x.get("submitted_at", datetime.min), reverse=True)
    
    return feedbacks

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(feedback_id: str):
    """
    Get a specific feedback by ID
    """
    feedbacks_collection = get_feedbacks_collection()
    users_collection = get_users_collection()
    
    # Find the feedback
    feedback = feedbacks_collection.find_one({"_id": ObjectId(feedback_id)})
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Format response
    feedback["id"] = str(feedback["_id"])
    del feedback["_id"]
    # Add computed fields
    feedback["likes_count"] = len(feedback.get("likes", []))
    feedback["dislikes_count"] = len(feedback.get("dislikes", []))
    # Ensure civilian_name is present
    if "civilian_name" not in feedback:
        civilian = users_collection.find_one({"_id": ObjectId(feedback["civilian_id"])})
        feedback["civilian_name"] = civilian["name"] if civilian else "Unknown User"
    
    return feedback