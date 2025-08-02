from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    experience_id = Column(Integer, ForeignKey("life_experiences.id"))
    
    # Reflection content
    what_surprised = Column(Text)
    how_felt = Column(Text)
    would_do_differently = Column(Text)
    key_insights = Column(Text)
    empathy_rating = Column(Integer)  # 1-10 scale
    
    # Additional thoughts
    free_form_notes = Column(Text)
    lessons_learned = Column(Text)
    
    # Sharing settings
    is_public = Column(Boolean, default=False)
    shared_on_social = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="reflections")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon_url = Column(String)
    category = Column(String)  # "exploration", "empathy", "diversity", etc.
    
    # Badge criteria
    criteria_type = Column(String)  # "experience_count", "category_diversity", "streak", etc.
    criteria_value = Column(Integer)  # threshold value
    
    # Badge properties
    rarity = Column(String)  # "common", "rare", "epic", "legendary"
    points_value = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_id = Column(Integer, ForeignKey("badges.id"))
    
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    experience_id = Column(Integer, ForeignKey("life_experiences.id"), nullable=True)  # Badge earned from specific experience
    
    # Relationships
    badge = relationship("Badge", back_populates="user_badges")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    challenge_type = Column(String)  # "daily", "weekly", "monthly", "special"
    
    # Challenge criteria
    target_category = Column(String)
    target_count = Column(Integer)
    target_region = Column(String)
    
    # Rewards
    points_reward = Column(Integer, default=0)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=True)
    
    # Timing
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    badge = relationship("Badge")
    user_challenges = relationship("UserChallenge", back_populates="challenge")

class UserChallenge(Base):
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    
    progress = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    challenge = relationship("Challenge", back_populates="user_challenges")