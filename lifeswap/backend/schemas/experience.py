from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class LifeExperienceBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    culture: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None
    cultural_context: Optional[str] = None
    learning_objectives: Optional[List[str]] = []
    tags: Optional[List[str]] = []

class LifeExperienceCreate(LifeExperienceBase):
    pass

class LifeExperienceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    region: Optional[str] = None
    culture: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None
    cultural_context: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None

class LifeExperience(LifeExperienceBase):
    id: int
    intro_video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    audio_narration_url: Optional[str] = None
    is_published: bool
    is_featured: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ScenarioChoiceBase(BaseModel):
    choice_text: str
    consequence_text: Optional[str] = None
    points_impact: int = 0
    choice_type: Optional[str] = None
    order_index: int = 0

class ScenarioChoiceCreate(ScenarioChoiceBase):
    next_scenario_id: Optional[int] = None

class ScenarioChoice(ScenarioChoiceBase):
    id: int
    next_scenario_id: Optional[int] = None

    class Config:
        from_attributes = True

class ScenarioBase(BaseModel):
    title: str
    content: str
    scenario_type: str = "info"
    order_index: int = 0
    points_awarded: int = 0
    time_limit: Optional[int] = None

class ScenarioCreate(ScenarioBase):
    experience_id: int
    parent_scenario_id: Optional[int] = None
    choices: List[ScenarioChoiceCreate] = []

class Scenario(ScenarioBase):
    id: int
    experience_id: int
    parent_scenario_id: Optional[int] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: datetime
    choices: List[ScenarioChoice] = []

    class Config:
        from_attributes = True

class UserExperienceBase(BaseModel):
    experience_id: int

class UserExperienceCreate(UserExperienceBase):
    pass

class UserExperience(UserExperienceBase):
    id: int
    user_id: int
    current_scenario_id: Optional[int] = None
    is_completed: bool
    completion_percentage: int
    points_earned: int
    choices_made: List[int] = []
    time_spent: int
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ExperienceProgress(BaseModel):
    experience_id: int
    scenario_id: int
    choice_id: Optional[int] = None
    time_spent: Optional[int] = None

class ExperienceComplete(BaseModel):
    experience_id: int
    total_time: int
    final_score: int