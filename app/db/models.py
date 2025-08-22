# app/db/models.py
from datetime import datetime, date
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

class HabitFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"

class HabitCategory(str, Enum):
    HEALTH = "health"
    PRODUCTIVITY = "productivity"
    LEARNING = "learning"
    SOCIAL = "social"
    WELLNESS = "wellness"
    OTHER = "other"

class LogStatus(str, Enum):
    COMPLETED = "completed"
    PARTIAL = "partial"
    SKIPPED = "skipped"

class Mood(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    OKAY = "okay"
    BAD = "bad"
    TERRIBLE = "terrible"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Gamification
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    avatar_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    habits = relationship("Habit", back_populates="user", cascade="all, delete-orphan")
    reflections = relationship("Reflection", back_populates="user", cascade="all, delete-orphan")
    challenge_memberships = relationship("ChallengeMember", back_populates="user")
    
    def calculate_level(self) -> int:
        """Calculate user level based on XP"""
        if self.xp < 100:
            return 1
        elif self.xp < 300:
            return 2
        elif self.xp < 600:
            return 3
        elif self.xp < 1000:
            return 4
        else:
            return 5 + ((self.xp - 1000) // 500)

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Habit details
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default=HabitCategory.OTHER)
    frequency = Column(String(20), default=HabitFrequency.DAILY)
    target_count = Column(Integer, default=1)  # How many times per frequency period
    
    # Progress tracking
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    total_completions = Column(Integer, default=0)
    
    # Settings
    is_active = Column(Boolean, default=True)
    reminder_time = Column(String(10), nullable=True)  # "09:00" format
    color = Column(String(7), default="#3B82F6")  # Hex color
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")
    
    def update_streak(self, completion_date: date) -> None:
        """Update streak counters based on completion date"""
        from datetime import timedelta
        
        # Get latest log before today
        latest_log = (
            session.query(HabitLog)
            .filter(HabitLog.habit_id == self.id, HabitLog.date < completion_date)
            .order_by(HabitLog.date.desc())
            .first()
        )
        
        if latest_log and latest_log.date == completion_date - timedelta(days=1):
            # Consecutive day, increment streak
            self.current_streak += 1
        else:
            # New streak starts
            self.current_streak = 1
            
        # Update best streak
        self.best_streak = max(self.best_streak, self.current_streak)

class HabitLog(Base):
    __tablename__ = "habit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = Column(UUID(as_uuid=True), ForeignKey("habits.id"), nullable=False, index=True)
    
    # Log details
    date = Column(Date, nullable=False, index=True)
    status = Column(String(20), default=LogStatus.COMPLETED)
    count = Column(Integer, default=1)  # How many times completed that day
    mood = Column(String(20), nullable=True)
    note = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    habit = relationship("Habit", back_populates="logs")
    
    # Unique constraint: one log per habit per day
    __table_args__ = (
        {"schema": None},
    )

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Challenge details
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default=HabitCategory.OTHER)
    
    # Duration
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Rewards
    reward_xp = Column(Integer, default=50)
    reward_badge = Column(String(100), nullable=True)
    
    # Settings
    is_active = Column(Boolean, default=True)
    max_members = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    members = relationship("ChallengeMember", back_populates="challenge", cascade="all, delete-orphan")
    
    @property
    def member_count(self) -> int:
        return len(self.members)
    
    @property
    def is_ongoing(self) -> bool:
        today = date.today()
        return self.start_date <= today <= self.end_date

class ChallengeMember(Base):
    __tablename__ = "challenge_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenge_id = Column(UUID(as_uuid=True), ForeignKey("challenges.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Progress tracking
    progress = Column(Float, default=0.0)  # Percentage 0-100
    completed_days = Column(Integer, default=0)
    total_days = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    completion_date = Column(DateTime, nullable=True)
    
    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    challenge = relationship("Challenge", back_populates="members")
    user = relationship("User", back_populates="challenge_memberships")
    
    # Unique constraint: one membership per user per challenge
    __table_args__ = (
        {"schema": None},
    )

class Reflection(Base):
    __tablename__ = "reflections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Reflection content
    date = Column(Date, nullable=False, index=True)
    mood = Column(String(20), nullable=False)
    energy_level = Column(Integer, nullable=True)  # 1-5 scale
    note = Column(Text, nullable=True)
    
    # Optional structured questions
    gratitude = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)
    tomorrow_focus = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reflections")
    
    # Unique constraint: one reflection per user per day
    __table_args__ = (
        {"schema": None},
    )

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Badge details
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=False)  # Icon name or emoji
    color = Column(String(7), default="#FFD700")  # Hex color
    
    # Requirements
    requirement_type = Column(String(50), nullable=False)  # "streak", "total", "challenge"
    requirement_value = Column(Integer, nullable=False)
    category = Column(String(50), nullable=True)
    
    # Settings
    is_active = Column(Boolean, default=True)
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id"), nullable=False, index=True)
    
    # Achievement details
    earned_at = Column(DateTime, default=datetime.utcnow)
    progress_snapshot = Column(Text, nullable=True)  # JSON string of progress when earned
    
    # Relationships
    user = relationship("User")
    badge = relationship("Badge")
    
    # Unique constraint: one badge per user
    __table_args__ = (
        {"schema": None},
    )