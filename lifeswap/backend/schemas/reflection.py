from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ReflectionBase(BaseModel):
    experience_id: int
    what_surprised: Optional[str] = None
    how_felt: Optional[str] = None
    would_do_differently: Optional[str] = None
    key_insights: Optional[str] = None
    empathy_rating: Optional[int] = None
    free_form_notes: Optional[str] = None
    lessons_learned: Optional[str] = None
    is_public: bool = False

class ReflectionCreate(ReflectionBase):
    pass

class ReflectionUpdate(BaseModel):
    what_surprised: Optional[str] = None
    how_felt: Optional[str] = None
    would_do_differently: Optional[str] = None
    key_insights: Optional[str] = None
    empathy_rating: Optional[int] = None
    free_form_notes: Optional[str] = None
    lessons_learned: Optional[str] = None
    is_public: Optional[bool] = None

class Reflection(ReflectionBase):
    id: int
    user_id: int
    shared_on_social: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BadgeBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    criteria_type: str
    criteria_value: int
    rarity: str = "common"
    points_value: int = 0

class BadgeCreate(BadgeBase):
    pass

class Badge(BadgeBase):
    id: int
    icon_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserBadge(BaseModel):
    id: int
    user_id: int
    badge_id: int
    earned_at: datetime
    experience_id: Optional[int] = None
    badge: Badge

    class Config:
        from_attributes = True

class ChallengeBase(BaseModel):
    title: str
    description: Optional[str] = None
    challenge_type: str
    target_category: Optional[str] = None
    target_count: int
    target_region: Optional[str] = None
    points_reward: int = 0
    start_date: datetime
    end_date: datetime

class ChallengeCreate(ChallengeBase):
    badge_id: Optional[int] = None

class Challenge(ChallengeBase):
    id: int
    badge_id: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserChallengeProgress(BaseModel):
    challenge_id: int
    progress: int
    is_completed: bool
    completed_at: Optional[datetime] = None
    challenge: Challenge

    class Config:
        from_attributes = True