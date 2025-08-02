from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from database.database import get_db
from models.user import User
from models.experience import LifeExperience, Scenario, ScenarioChoice
from models.reflection import Badge, Challenge
from schemas.experience import LifeExperienceCreate, LifeExperienceUpdate, ScenarioCreate
from schemas.reflection import BadgeCreate, ChallengeCreate
from utils.auth import get_current_admin_user

router = APIRouter()

# Life Experience Management
@router.post("/experiences", response_model=dict)
async def create_experience(
    experience: LifeExperienceCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new life experience."""
    db_experience = LifeExperience(
        **experience.dict(exclude={"learning_objectives", "tags"}),
        learning_objectives=json.dumps(experience.learning_objectives or []),
        tags=json.dumps(experience.tags or [])
    )
    
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    
    return {"id": db_experience.id, "message": "Experience created successfully"}

@router.put("/experiences/{experience_id}")
async def update_experience(
    experience_id: int,
    experience_update: LifeExperienceUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update a life experience."""
    experience = db.query(LifeExperience).filter(LifeExperience.id == experience_id).first()
    
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    for field, value in experience_update.dict(exclude_unset=True).items():
        if field in ["learning_objectives", "tags"] and value is not None:
            setattr(experience, field, json.dumps(value))
        else:
            setattr(experience, field, value)
    
    db.commit()
    
    return {"message": "Experience updated successfully"}

# Scenario Management
@router.post("/scenarios")
async def create_scenario(
    scenario: ScenarioCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new scenario."""
    db_scenario = Scenario(
        **scenario.dict(exclude={"choices"})
    )
    
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    
    # Add choices
    for choice in scenario.choices:
        db_choice = ScenarioChoice(
            scenario_id=db_scenario.id,
            **choice.dict()
        )
        db.add(db_choice)
    
    db.commit()
    
    return {"id": db_scenario.id, "message": "Scenario created successfully"}

# Badge Management
@router.post("/badges")
async def create_badge(
    badge: BadgeCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new badge."""
    db_badge = Badge(**badge.dict())
    
    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    
    return {"id": db_badge.id, "message": "Badge created successfully"}

# Challenge Management
@router.post("/challenges")
async def create_challenge(
    challenge: ChallengeCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new challenge."""
    db_challenge = Challenge(**challenge.dict())
    
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    
    return {"id": db_challenge.id, "message": "Challenge created successfully"}

# Analytics
@router.get("/analytics")
async def get_analytics(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get platform analytics."""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_experiences = db.query(LifeExperience).count()
    published_experiences = db.query(LifeExperience).filter(LifeExperience.is_published == True).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_experiences": total_experiences,
        "published_experiences": published_experiences,
        "completion_rate": 75.5  # Placeholder - calculate actual rate
    }