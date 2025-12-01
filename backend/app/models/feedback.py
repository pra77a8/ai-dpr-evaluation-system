from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class FeedbackBase(BaseModel):
    dpr_id: str
    project_title: str
    civilian_id: str  # User ID of the civilian submitting feedback
    content: str

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackInDB(FeedbackBase):
    id: str
    submitted_at: datetime
    likes: List[str] = []  # List of user IDs who liked the feedback
    dislikes: List[str] = []  # List of user IDs who disliked the feedback

class FeedbackResponse(FeedbackBase):
    id: str
    submitted_at: datetime
    likes: List[str] = []
    dislikes: List[str] = []
    likes_count: int = 0
    dislikes_count: int = 0
    civilian_name: str = ""  # Added to show civilian name