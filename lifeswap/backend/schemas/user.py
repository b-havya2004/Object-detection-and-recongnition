from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    country: Optional[str] = None
    age_group: Optional[str] = None
    interests: Optional[List[str]] = []

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    country: Optional[str] = None
    age_group: Optional[str] = None
    interests: Optional[List[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    empathy_points: int
    total_experiences: int
    badges: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfile(User):
    experiences_completed: List["UserExperience"] = []
    reflections: List["Reflection"] = []

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Import here to avoid circular imports
from .experience import UserExperience
from .reflection import Reflection