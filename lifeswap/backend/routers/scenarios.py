from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from models.experience import Scenario, ScenarioChoice
from schemas.experience import Scenario as ScenarioSchema

router = APIRouter()

@router.get("/{scenario_id}", response_model=ScenarioSchema)
async def get_scenario(scenario_id: int, db: Session = Depends(get_db)):
    """Get a specific scenario with its choices."""
    scenario = db.query(Scenario).filter(Scenario.id == scenario_id).first()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return scenario

@router.get("/experience/{experience_id}", response_model=List[ScenarioSchema])
async def get_experience_scenarios(
    experience_id: int, 
    db: Session = Depends(get_db)
):
    """Get all scenarios for an experience."""
    scenarios = db.query(Scenario).filter(
        Scenario.experience_id == experience_id
    ).order_by(Scenario.order_index).all()
    
    return scenarios