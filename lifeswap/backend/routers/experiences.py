from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database.database import get_db
from models.user import User
from models.experience import LifeExperience, UserExperience, Scenario
from schemas.experience import (
    LifeExperience as LifeExperienceSchema,
    UserExperience as UserExperienceSchema,
    UserExperienceCreate,
    ExperienceProgress,
    ExperienceComplete
)
from utils.auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[LifeExperienceSchema])
async def get_experiences(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    region: Optional[str] = None,
    difficulty: Optional[str] = None,
    featured: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of published life experiences with filters."""
    query = db.query(LifeExperience).filter(LifeExperience.is_published == True)
    
    if category:
        query = query.filter(LifeExperience.category == category)
    if region:
        query = query.filter(LifeExperience.region == region)
    if difficulty:
        query = query.filter(LifeExperience.difficulty_level == difficulty)
    if featured is not None:
        query = query.filter(LifeExperience.is_featured == featured)
    
    experiences = query.offset(skip).limit(limit).all()
    return experiences

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get available experience categories."""
    categories = db.query(LifeExperience.category).filter(
        LifeExperience.is_published == True,
        LifeExperience.category.isnot(None)
    ).distinct().all()
    
    return [cat[0] for cat in categories if cat[0]]

@router.get("/regions")
async def get_regions(db: Session = Depends(get_db)):
    """Get available experience regions."""
    regions = db.query(LifeExperience.region).filter(
        LifeExperience.is_published == True,
        LifeExperience.region.isnot(None)
    ).distinct().all()
    
    return [region[0] for region in regions if region[0]]

@router.get("/{experience_id}", response_model=LifeExperienceSchema)
async def get_experience(experience_id: int, db: Session = Depends(get_db)):
    """Get a specific life experience."""
    experience = db.query(LifeExperience).filter(
        LifeExperience.id == experience_id,
        LifeExperience.is_published == True
    ).first()
    
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    return experience

@router.post("/{experience_id}/start", response_model=UserExperienceSchema)
async def start_experience(
    experience_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start a new life experience."""
    # Check if experience exists and is published
    experience = db.query(LifeExperience).filter(
        LifeExperience.id == experience_id,
        LifeExperience.is_published == True
    ).first()
    
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    # Check if user already has an ongoing experience
    existing = db.query(UserExperience).filter(
        UserExperience.user_id == current_user.id,
        UserExperience.experience_id == experience_id,
        UserExperience.is_completed == False
    ).first()
    
    if existing:
        return existing
    
    # Get the first scenario
    first_scenario = db.query(Scenario).filter(
        Scenario.experience_id == experience_id,
        Scenario.parent_scenario_id.is_(None)
    ).order_by(Scenario.order_index).first()
    
    # Create new user experience
    user_experience = UserExperience(
        user_id=current_user.id,
        experience_id=experience_id,
        current_scenario_id=first_scenario.id if first_scenario else None,
        choices_made=json.dumps([])
    )
    
    db.add(user_experience)
    db.commit()
    db.refresh(user_experience)
    
    return user_experience

@router.post("/{experience_id}/progress")
async def update_progress(
    experience_id: int,
    progress: ExperienceProgress,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user progress in an experience."""
    # Get user experience
    user_experience = db.query(UserExperience).filter(
        UserExperience.user_id == current_user.id,
        UserExperience.experience_id == experience_id,
        UserExperience.is_completed == False
    ).first()
    
    if not user_experience:
        raise HTTPException(status_code=404, detail="Experience not started")
    
    # Update current scenario
    user_experience.current_scenario_id = progress.scenario_id
    
    # Add choice to choices made
    if progress.choice_id:
        choices = json.loads(user_experience.choices_made or "[]")
        choices.append(progress.choice_id)
        user_experience.choices_made = json.dumps(choices)
    
    # Update time spent
    if progress.time_spent:
        user_experience.time_spent += progress.time_spent
    
    # Calculate completion percentage (simplified)
    total_scenarios = db.query(Scenario).filter(Scenario.experience_id == experience_id).count()
    completed_scenarios = len(json.loads(user_experience.choices_made or "[]"))
    user_experience.completion_percentage = min(100, (completed_scenarios / total_scenarios) * 100)
    
    db.commit()
    
    return {"message": "Progress updated successfully"}

@router.post("/{experience_id}/complete")
async def complete_experience(
    experience_id: int,
    completion: ExperienceComplete,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Complete a life experience."""
    # Get user experience
    user_experience = db.query(UserExperience).filter(
        UserExperience.user_id == current_user.id,
        UserExperience.experience_id == experience_id,
        UserExperience.is_completed == False
    ).first()
    
    if not user_experience:
        raise HTTPException(status_code=404, detail="Experience not started")
    
    # Mark as completed
    user_experience.is_completed = True
    user_experience.completion_percentage = 100
    user_experience.points_earned = completion.final_score
    user_experience.time_spent = completion.total_time
    
    # Update user stats
    current_user.empathy_points += completion.final_score
    current_user.total_experiences += 1
    
    db.commit()
    
    return {"message": "Experience completed", "points_earned": completion.final_score}

@router.get("/my/experiences", response_model=List[UserExperienceSchema])
async def get_my_experiences(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's experiences."""
    experiences = db.query(UserExperience).filter(
        UserExperience.user_id == current_user.id
    ).all()
    
    return experiences