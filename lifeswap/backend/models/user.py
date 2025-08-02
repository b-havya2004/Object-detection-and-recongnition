from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    country = Column(String)
    age_group = Column(String)  # "18-25", "26-35", etc.
    interests = Column(Text)  # JSON string of interests
    
    # Profile stats
    empathy_points = Column(Integer, default=0)
    total_experiences = Column(Integer, default=0)
    badges = Column(Text)  # JSON string of earned badges
    
    # Account settings
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    experiences_completed = relationship("UserExperience", back_populates="user")
    reflections = relationship("Reflection", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")