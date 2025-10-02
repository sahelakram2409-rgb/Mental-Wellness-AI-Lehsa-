"""
SQLAlchemy database models for the Mental Wellness API.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
    Float,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User model for storing user information."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    display_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    mood_entries = relationship("MoodEntry", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    journal_entries = relationship("JournalEntry", back_populates="user", cascade="all, delete-orphan")


class MoodEntry(Base):
    """Model for storing user mood entries."""
    
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    mood_level = Column(Integer, nullable=False)  # 1-10 scale
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="mood_entries")


class ChatMessage(Base):
    """Model for storing chat conversations."""
    
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    mood_context = Column(Text, nullable=True)  # JSON string of mood context used
    ai_provider = Column(String(100), nullable=False)
    ai_model = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chat_messages")


class JournalEntry(Base):
    """Model for storing private journal entries."""
    
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    ai_summary = Column(Text, nullable=True)  # Optional AI-generated summary
    is_private = Column(Boolean, default=True, nullable=False)
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="journal_entries")


class ExerciseSession(Base):
    """Model for tracking guided exercise sessions."""
    
    __tablename__ = "exercise_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    exercise_type = Column(String(100), nullable=False)  # breathing, meditation, etc.
    exercise_name = Column(String(255), nullable=False)
    duration_minutes = Column(Float, nullable=True)
    completion_status = Column(String(50), default="completed")  # completed, partial, skipped
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="exercise_sessions")


# Add the relationship to User model
User.exercise_sessions = relationship("ExerciseSession", back_populates="user", cascade="all, delete-orphan")


class MusicSession(Base):
    """Model for tracking music/piano learning sessions."""
    
    __tablename__ = "music_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.user_id"), nullable=False, index=True)
    session_type = Column(String(100), nullable=False)  # practice, lesson, free_play
    song_name = Column(String(255), nullable=True)
    difficulty_level = Column(String(50), nullable=True)  # beginner, intermediate, advanced
    duration_minutes = Column(Float, nullable=True)
    progress_score = Column(Float, nullable=True)  # 0-100 score
    ai_feedback = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="music_sessions")


# Add the relationship to User model
User.music_sessions = relationship("MusicSession", back_populates="user", cascade="all, delete-orphan")