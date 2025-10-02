"""
Repository pattern implementation for database operations.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
import json
import logging

from models.database import User, MoodEntry, ChatMessage, JournalEntry, ExerciseSession, MusicSession
from models.schemas import MoodEntry as MoodEntrySchema

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user_id: str, email: Optional[str] = None, display_name: Optional[str] = None) -> User:
        """Create a new user or return existing one."""
        user = self.get_user_by_id(user_id)
        if user:
            return user
        
        user = User(
            user_id=user_id,
            email=email,
            display_name=display_name
        )
        self.session.add(user)
        self.session.flush()  # Get the ID without committing
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by user_id."""
        return self.session.query(User).filter(User.user_id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.session.query(User).filter(User.email == email).first()
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user information."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user and all associated data."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.session.delete(user)
        return True


class MoodRepository:
    """Repository for mood entry operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_mood_entry(self, user_id: str, mood_level: int, notes: Optional[str] = None, timestamp: Optional[datetime] = None) -> MoodEntry:
        """Create a new mood entry."""
        # Ensure user exists
        user_repo = UserRepository(self.session)
        user_repo.create_user(user_id)
        
        mood_entry = MoodEntry(
            user_id=user_id,
            mood_level=mood_level,
            notes=notes
        )
        
        if timestamp:
            mood_entry.timestamp = timestamp
        
        self.session.add(mood_entry)
        self.session.flush()
        return mood_entry
    
    def get_mood_entries_by_user(self, user_id: str, days_back: int = 7, limit: Optional[int] = None) -> List[MoodEntry]:
        """Get mood entries for a user within the last N days."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        query = (
            self.session.query(MoodEntry)
            .filter(
                and_(
                    MoodEntry.user_id == user_id,
                    MoodEntry.timestamp >= cutoff_date
                )
            )
            .order_by(MoodEntry.timestamp)
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def get_mood_entry_by_id(self, mood_id: int) -> Optional[MoodEntry]:
        """Get mood entry by ID."""
        return self.session.query(MoodEntry).filter(MoodEntry.id == mood_id).first()
    
    def get_user_mood_statistics(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get mood statistics for a user."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        result = (
            self.session.query(
                func.count(MoodEntry.id).label('total_entries'),
                func.avg(MoodEntry.mood_level).label('average_mood'),
                func.min(MoodEntry.mood_level).label('min_mood'),
                func.max(MoodEntry.mood_level).label('max_mood')
            )
            .filter(
                and_(
                    MoodEntry.user_id == user_id,
                    MoodEntry.timestamp >= cutoff_date
                )
            )
            .first()
        )
        
        return {
            'total_entries': result.total_entries or 0,
            'average_mood': float(result.average_mood) if result.average_mood else 0,
            'min_mood': result.min_mood or 0,
            'max_mood': result.max_mood or 0,
            'days_analyzed': days_back
        }
    
    def delete_mood_entry(self, mood_id: int) -> bool:
        """Delete a mood entry."""
        mood_entry = self.get_mood_entry_by_id(mood_id)
        if not mood_entry:
            return False
        
        self.session.delete(mood_entry)
        return True


class ChatRepository:
    """Repository for chat message operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_chat_message(
        self, 
        user_id: str, 
        message: str, 
        response: str, 
        ai_provider: str, 
        ai_model: str,
        mood_context: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        """Create a new chat message record."""
        # Ensure user exists
        user_repo = UserRepository(self.session)
        user_repo.create_user(user_id)
        
        chat_message = ChatMessage(
            user_id=user_id,
            message=message,
            response=response,
            ai_provider=ai_provider,
            ai_model=ai_model,
            mood_context=json.dumps(mood_context) if mood_context else None
        )
        
        self.session.add(chat_message)
        self.session.flush()
        return chat_message
    
    def get_chat_history_by_user(self, user_id: str, limit: int = 50) -> List[ChatMessage]:
        """Get recent chat history for a user."""
        return (
            self.session.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(desc(ChatMessage.timestamp))
            .limit(limit)
            .all()
        )
    
    def get_chat_message_by_id(self, message_id: int) -> Optional[ChatMessage]:
        """Get chat message by ID."""
        return self.session.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    
    def delete_chat_message(self, message_id: int) -> bool:
        """Delete a chat message."""
        message = self.get_chat_message_by_id(message_id)
        if not message:
            return False
        
        self.session.delete(message)
        return True
    
    def get_user_chat_statistics(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get chat statistics for a user."""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        result = (
            self.session.query(func.count(ChatMessage.id))
            .filter(
                and_(
                    ChatMessage.user_id == user_id,
                    ChatMessage.timestamp >= cutoff_date
                )
            )
            .scalar()
        )
        
        return {
            'total_messages': result or 0,
            'days_analyzed': days_back
        }


class JournalRepository:
    """Repository for journal entry operations."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_journal_entry(
        self, 
        user_id: str, 
        content: str, 
        title: Optional[str] = None,
        tags: Optional[str] = None,
        is_private: bool = True
    ) -> JournalEntry:
        """Create a new journal entry."""
        # Ensure user exists
        user_repo = UserRepository(self.session)
        user_repo.create_user(user_id)
        
        journal_entry = JournalEntry(
            user_id=user_id,
            content=content,
            title=title,
            tags=tags,
            is_private=is_private
        )
        
        self.session.add(journal_entry)
        self.session.flush()
        return journal_entry
    
    def get_journal_entries_by_user(self, user_id: str, limit: Optional[int] = None) -> List[JournalEntry]:
        """Get journal entries for a user."""
        query = (
            self.session.query(JournalEntry)
            .filter(JournalEntry.user_id == user_id)
            .order_by(desc(JournalEntry.timestamp))
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def get_journal_entry_by_id(self, entry_id: int) -> Optional[JournalEntry]:
        """Get journal entry by ID."""
        return self.session.query(JournalEntry).filter(JournalEntry.id == entry_id).first()
    
    def update_journal_entry(self, entry_id: int, **kwargs) -> Optional[JournalEntry]:
        """Update journal entry."""
        entry = self.get_journal_entry_by_id(entry_id)
        if not entry:
            return None
        
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
        
        entry.updated_at = datetime.utcnow()
        return entry
    
    def delete_journal_entry(self, entry_id: int) -> bool:
        """Delete a journal entry."""
        entry = self.get_journal_entry_by_id(entry_id)
        if not entry:
            return False
        
        self.session.delete(entry)
        return True


def convert_mood_entry_to_schema(db_mood: MoodEntry) -> MoodEntrySchema:
    """Convert database MoodEntry to Pydantic schema."""
    return MoodEntrySchema(
        user_id=db_mood.user_id,
        mood_level=db_mood.mood_level,
        notes=db_mood.notes,
        timestamp=db_mood.timestamp
    )