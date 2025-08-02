from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database.database import get_db
from models.user import User
from schemas.user import User as UserSchema, UserUpdate
from utils.auth import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user profile."""
    return current_user

@router.put("/me", response_model=UserSchema)
async def update_users_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile."""
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "interests":
            setattr(current_user, field, json.dumps(value))
        else:
            setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/leaderboard", response_model=List[dict])
async def get_leaderboard(
    limit: int = 10,
    category: str = "empathy_points",
    db: Session = Depends(get_db)
):
    """Get user leaderboard."""
    if category == "empathy_points":
        users = db.query(User).filter(User.is_active == True).order_by(User.empathy_points.desc()).limit(limit).all()
    elif category == "total_experiences":
        users = db.query(User).filter(User.is_active == True).order_by(User.total_experiences.desc()).limit(limit).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    leaderboard = []
    for i, user in enumerate(users, 1):
        leaderboard.append({
            "rank": i,
            "username": user.username,
            "empathy_points": user.empathy_points,
            "total_experiences": user.total_experiences,
            "country": user.country
        })
    
    return leaderboard

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user statistics and progress."""
    # Get user's badges
    badges = json.loads(current_user.badges or "[]")
    
    # Calculate completion rate
    total_experiences = current_user.total_experiences
    completion_rate = min(100, (total_experiences / 10) * 100) if total_experiences > 0 else 0
    
    return {
        "empathy_points": current_user.empathy_points,
        "total_experiences": total_experiences,
        "badges_count": len(badges),
        "completion_rate": completion_rate,
        "level": min(10, total_experiences // 2 + 1),
        "next_level_requirement": (total_experiences // 2 + 1) * 2
    }