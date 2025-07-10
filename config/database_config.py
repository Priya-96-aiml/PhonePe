"""
Database configuration and connection management.
"""

import sqlite3
import os
from sqlalchemy import create_engine
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConfig:
    """Database configuration and connection management."""
    
    def __init__(self, db_path: str = "data/analytics.db"):
        """
        Initialize database configuration.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.engine = None
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get SQLite database connection.
        
        Returns:
            sqlite3.Connection: Database connection
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            return conn
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def get_engine(self):
        """
        Get SQLAlchemy engine for pandas integration.
        
        Returns:
            sqlalchemy.Engine: Database engine
        """
        if self.engine is None:
            self.engine = create_engine(f'sqlite:///{self.db_path}')
        return self.engine
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """
        Execute SQL query and return results.
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            
        Returns:
            list: Query results
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    
    def execute_script(self, script_path: str):
        """
        Execute SQL script from file.
        
        Args:
            script_path (str): Path to SQL script file
        """
        with open(script_path, 'r') as file:
            script = file.read()
        
        with self.get_connection() as conn:
            conn.executescript(script)
            conn.commit()
            logger.info(f"Executed script: {script_path}")

# Global database instance
db_config = DatabaseConfig()