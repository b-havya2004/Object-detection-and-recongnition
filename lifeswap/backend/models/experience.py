from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class LifeExperience(Base):
    __tablename__ = "life_experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # "refugee", "disability", "profession", etc.
    region = Column(String)
    culture = Column(String)
    difficulty_level = Column(String)  # "beginner", "intermediate", "advanced"
    estimated_duration = Column(Integer)  # in minutes
    
    # Media
    intro_video_url = Column(String)
    thumbnail_url = Column(String)
    audio_narration_url = Column(String)
    
    # Content
    cultural_context = Column(Text)
    learning_objectives = Column(Text)  # JSON string
    tags = Column(Text)  # JSON string of tags
    
    # Status
    is_published = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    scenarios = relationship("Scenario", back_populates="experience")
    user_experiences = relationship("UserExperience", back_populates="experience")

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("life_experiences.id"))
    
    # Scenario content
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    scenario_type = Column(String)  # "decision", "info", "reflection"
    order_index = Column(Integer, default=0)
    
    # Decision logic
    parent_scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=True)
    condition = Column(Text)  # JSON condition for branching
    points_awarded = Column(Integer, default=0)
    
    # Media
    image_url = Column(String)
    audio_url = Column(String)
    
    # Timing
    time_limit = Column(Integer)  # seconds for timed decisions
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    experience = relationship("LifeExperience", back_populates="scenarios")
    parent = relationship("Scenario", remote_side=[id])
    children = relationship("Scenario")
    choices = relationship("ScenarioChoice", back_populates="scenario")

class ScenarioChoice(Base):
    __tablename__ = "scenario_choices"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(Integer, ForeignKey("scenarios.id"))
    
    choice_text = Column(String, nullable=False)
    consequence_text = Column(Text)
    points_impact = Column(Integer, default=0)
    next_scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=True)
    
    # Choice metadata
    choice_type = Column(String)  # "empathetic", "practical", "risky", etc.
    order_index = Column(Integer, default=0)

    # Relationships
    scenario = relationship("Scenario", back_populates="choices", foreign_keys=[scenario_id])
    next_scenario = relationship("Scenario", foreign_keys=[next_scenario_id])

class UserExperience(Base):
    __tablename__ = "user_experiences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    experience_id = Column(Integer, ForeignKey("life_experiences.id"))
    
    # Progress tracking
    current_scenario_id = Column(Integer, ForeignKey("scenarios.id"), nullable=True)
    is_completed = Column(Boolean, default=False)
    completion_percentage = Column(Integer, default=0)
    points_earned = Column(Integer, default=0)
    
    # Journey data
    choices_made = Column(Text)  # JSON array of choice IDs
    time_spent = Column(Integer, default=0)  # seconds
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="experiences_completed")
    experience = relationship("LifeExperience", back_populates="user_experiences")
    current_scenario = relationship("Scenario")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Daily/weekly tracking
    daily_experiences = Column(Integer, default=0)
    weekly_experiences = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    
    # Category progress
    categories_explored = Column(Text)  # JSON object with category: count
    regions_explored = Column(Text)  # JSON object with region: count
    
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    week_start = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="progress")