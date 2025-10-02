#!/usr/bin/env python3
"""
Database initialization script for Mental Wellness API.
"""
import logging
from services.database import init_db, DatabaseManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Initialize the database."""
    try:
        logger.info("Initializing database...")
        
        # Initialize database
        init_db()
        
        # Get connection info
        conn_info = DatabaseManager.get_connection_info()
        logger.info(f"Database initialized successfully!")
        logger.info(f"Database URL: {conn_info['database_url']}")
        logger.info(f"Database type: {'SQLite' if conn_info['is_sqlite'] else 'PostgreSQL'}")
        
        # Test database health
        if DatabaseManager.health_check():
            logger.info("Database health check: PASSED ✅")
        else:
            logger.error("Database health check: FAILED ❌")
            return 1
        
        logger.info("Database initialization completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())