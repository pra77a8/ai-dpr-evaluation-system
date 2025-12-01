from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from bson import ObjectId

class UserRole(str, Enum):
    ORGANIZATION = "Organization"
    CIVILIAN = "Civilian"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str

class UserResponse(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: UserRole

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None