"""
Database configuration and session management.
"""
import os
from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import logging

from models.database import Base

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Database configuration based on environment."""
    
    def __init__(self):
        self.database_url = self._get_database_url()
        self.async_database_url = self._get_async_database_url()
        self.engine = None
        self.async_engine = None
        self.SessionLocal = None
        self.AsyncSessionLocal = None
        
    def _get_database_url(self) -> str:
        """Get database URL based on environment."""
        # Check for explicit database URL
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")
        
        # Development: use SQLite
        if os.getenv("ENVIRONMENT", "development") == "development":
            db_path = os.path.join(os.getcwd(), "mental_wellness.db")
            return f"sqlite:///{db_path}"
        
        # Production: use PostgreSQL
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "mental_wellness")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "")
        
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    def _get_async_database_url(self) -> str:
        """Get async database URL."""
        url = self._get_database_url()
        
        if url.startswith("sqlite://"):
            return url.replace("sqlite://", "sqlite+aiosqlite://")
        elif url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://")
        
        return url
    
    def initialize(self):
        """Initialize database engines and sessions."""
        # Synchronous engine (for migrations and simple operations)
        if self.database_url.startswith("sqlite"):
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
            )
        else:
            self.engine = create_engine(
                self.database_url,
                echo=os.getenv("SQL_DEBUG", "false").lower() == "true"
            )
        
        # Session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info(f"Database initialized with URL: {self.database_url}")
    
    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created")
    
    def drop_tables(self):
        """Drop all tables (use with caution!)."""
        Base.metadata.drop_all(bind=self.engine)
        logger.info("Database tables dropped")


# Global database configuration
db_config = DatabaseConfig()


def get_database_url() -> str:
    """Get the current database URL."""
    return db_config.database_url


def init_db():
    """Initialize the database."""
    db_config.initialize()
    db_config.create_tables()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get a database session with automatic cleanup."""
    if not db_config.SessionLocal:
        init_db()
    
    session = db_config.SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database session error: {e}")
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for getting database sessions."""
    if not db_config.SessionLocal:
        init_db()
    
    session = db_config.SessionLocal()
    try:
        yield session
        session.commit()  # Ensure changes are committed
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()


class DatabaseManager:
    """High-level database management utilities."""
    
    @staticmethod
    def reset_database():
        """Reset the database (drop and recreate all tables)."""
        logger.warning("Resetting database - all data will be lost!")
        db_config.drop_tables()
        db_config.create_tables()
    
    @staticmethod
    def get_connection_info() -> dict:
        """Get database connection information."""
        return {
            "database_url": db_config.database_url,
            "engine_info": str(db_config.engine.url) if db_config.engine else None,
            "is_sqlite": db_config.database_url.startswith("sqlite"),
            "is_postgresql": db_config.database_url.startswith("postgresql")
        }
    
    @staticmethod
    def health_check() -> bool:
        """Check if database is accessible."""
        try:
            from sqlalchemy import text
            with get_db_session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
