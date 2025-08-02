from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.user import User
from models.reflection import Reflection
from schemas.reflection import (
    ReflectionCreate, 
    ReflectionUpdate, 
    Reflection as ReflectionSchema
)
from utils.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=ReflectionSchema)
async def create_reflection(
    reflection: ReflectionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new reflection."""
    db_reflection = Reflection(
        user_id=current_user.id,
        **reflection.dict()
    )
    
    db.add(db_reflection)
    db.commit()
    db.refresh(db_reflection)
    
    return db_reflection

@router.get("/", response_model=List[ReflectionSchema])
async def get_my_reflections(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's reflections."""
    reflections = db.query(Reflection).filter(
        Reflection.user_id == current_user.id
    ).all()
    
    return reflections

@router.get("/public", response_model=List[ReflectionSchema])
async def get_public_reflections(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get public reflections from all users."""
    reflections = db.query(Reflection).filter(
        Reflection.is_public == True
    ).offset(skip).limit(limit).all()
    
    return reflections

@router.put("/{reflection_id}", response_model=ReflectionSchema)
async def update_reflection(
    reflection_id: int,
    reflection_update: ReflectionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a reflection."""
    reflection = db.query(Reflection).filter(
        Reflection.id == reflection_id,
        Reflection.user_id == current_user.id
    ).first()
    
    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")
    
    for field, value in reflection_update.dict(exclude_unset=True).items():
        setattr(reflection, field, value)
    
    db.commit()
    db.refresh(reflection)
    
    return reflection