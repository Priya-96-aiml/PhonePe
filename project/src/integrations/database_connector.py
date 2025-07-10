"""
Database connector for multiple database systems.
Supports PostgreSQL, MySQL, MongoDB, and cloud databases.
"""

import logging
from typing import Dict, List, Optional, Any, Union
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import pymongo
from pymongo import MongoClient
import psycopg2
import mysql.connector
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Database connection configuration."""
    db_type: str  # postgresql, mysql, mongodb, sqlite
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_mode: str = 'prefer'
    connection_pool_size: int = 5

class DatabaseConnector:
    """Universal database connector supporting multiple database systems."""
    
    def __init__(self):
        self.connections = {}
        self.engines = {}
    
    def add_connection(self, name: str, config: DatabaseConfig):
        """Add a new database connection."""
        try:
            if config.db_type == 'postgresql':
                connection_string = (
                    f"postgresql://{config.username}:{config.password}@"
                    f"{config.host}:{config.port}/{config.database}"
                )
                engine = create_engine(
                    connection_string,
                    pool_size=config.connection_pool_size,
                    echo=False
                )
                self.engines[name] = engine
                
            elif config.db_type == 'mysql':
                connection_string = (
                    f"mysql+pymysql://{config.username}:{config.password}@"
                    f"{config.host}:{config.port}/{config.database}"
                )
                engine = create_engine(
                    connection_string,
                    pool_size=config.connection_pool_size,
                    echo=False
                )
                self.engines[name] = engine
                
            elif config.db_type == 'mongodb':
                connection_string = (
                    f"mongodb://{config.username}:{config.password}@"
                    f"{config.host}:{config.port}/{config.database}"
                )
                client = MongoClient(connection_string)
                self.connections[name] = client[config.database]
                
            elif config.db_type == 'sqlite':
                connection_string = f"sqlite:///{config.database}"
                engine = create_engine(connection_string)
                self.engines[name] = engine
                
            logger.info(f"Added {config.db_type} connection: {name}")
            
        except Exception as e:
            logger.error(f"Failed to create connection {name}: {e}")
            raise
    
    def execute_query(self, connection_name: str, query: str, params: Dict = None) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame."""
        if connection_name not in self.engines:
            raise ValueError(f"Connection {connection_name} not found")
            
        engine = self.engines[connection_name]
        
        try:
            if params:
                result = pd.read_sql_query(text(query), engine, params=params)
            else:
                result = pd.read_sql_query(query, engine)
                
            logger.info(f"Query executed successfully on {connection_name}")
            return result
            
        except Exception as e:
            logger.error(f"Query execution failed on {connection_name}: {e}")
            raise
    
    def execute_mongo_query(self, connection_name: str, collection: str, 
                          query: Dict, limit: int = 1000) -> pd.DataFrame:
        """Execute MongoDB query and return results as DataFrame."""
        if connection_name not in self.connections:
            raise ValueError(f"MongoDB connection {connection_name} not found")
            
        db = self.connections[connection_name]
        
        try:
            cursor = db[collection].find(query).limit(limit)
            data = list(cursor)
            
            # Convert ObjectId to string for DataFrame compatibility
            for doc in data:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])
                    
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"MongoDB query failed on {connection_name}: {e}")
            raise
    
    def bulk_insert(self, connection_name: str, table_name: str, 
                   data: pd.DataFrame, if_exists: str = 'append'):
        """Bulk insert DataFrame into database table."""
        if connection_name not in self.engines:
            raise ValueError(f"Connection {connection_name} not found")
            
        engine = self.engines[connection_name]
        
        try:
            data.to_sql(table_name, engine, if_exists=if_exists, index=False)
            logger.info(f"Bulk insert completed: {len(data)} rows to {table_name}")
            
        except Exception as e:
            logger.error(f"Bulk insert failed: {e}")
            raise
    
    def get_table_schema(self, connection_name: str, table_name: str) -> pd.DataFrame:
        """Get table schema information."""
        if connection_name not in self.engines:
            raise ValueError(f"Connection {connection_name} not found")
            
        engine = self.engines[connection_name]
        
        # Get database type from engine
        db_type = engine.dialect.name
        
        if db_type == 'postgresql':
            query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = :table_name
                ORDER BY ordinal_position
            """
        elif db_type == 'mysql':
            query = """
                SELECT COLUMN_NAME as column_name, DATA_TYPE as data_type, 
                       IS_NULLABLE as is_nullable, COLUMN_DEFAULT as column_default
                FROM information_schema.COLUMNS
                WHERE TABLE_NAME = :table_name
                ORDER BY ORDINAL_POSITION
            """
        else:
            # SQLite
            query = f"PRAGMA table_info({table_name})"
            
        return self.execute_query(connection_name, query, {'table_name': table_name})
    
    def test_connection(self, connection_name: str) -> bool:
        """Test database connection."""
        try:
            if connection_name in self.engines:
                # Test SQL connection
                self.execute_query(connection_name, "SELECT 1 as test")
            elif connection_name in self.connections:
                # Test MongoDB connection
                db = self.connections[connection_name]
                db.command('ping')
            else:
                return False
                
            logger.info(f"Connection test successful: {connection_name}")
            return True
            
        except Exception as e:
            logger.error(f"Connection test failed for {connection_name}: {e}")
            return False
    
    def close_connections(self):
        """Close all database connections."""
        for name, engine in self.engines.items():
            engine.dispose()
            logger.info(f"Closed SQL connection: {name}")
            
        for name, client in self.connections.items():
            client.close()
            logger.info(f"Closed MongoDB connection: {name}")
            
        self.engines.clear()
        self.connections.clear()

# Cloud database integrations
class AWSRDSConnector(DatabaseConnector):
    """AWS RDS database connector."""
    
    def connect_rds_postgres(self, name: str, endpoint: str, database: str, 
                           username: str, password: str, port: int = 5432):
        """Connect to AWS RDS PostgreSQL instance."""
        config = DatabaseConfig(
            db_type='postgresql',
            host=endpoint,
            port=port,
            database=database,
            username=username,
            password=password,
            ssl_mode='require'
        )
        self.add_connection(name, config)

class AzureSQLConnector(DatabaseConnector):
    """Azure SQL Database connector."""
    
    def connect_azure_sql(self, name: str, server: str, database: str, 
                         username: str, password: str):
        """Connect to Azure SQL Database."""
        config = DatabaseConfig(
            db_type='mssql',
            host=f"{server}.database.windows.net",
            port=1433,
            database=database,
            username=username,
            password=password,
            ssl_mode='require'
        )
        # Use pyodbc driver for SQL Server
        connection_string = (
            f"mssql+pyodbc://{username}:{password}@"
            f"{server}.database.windows.net:1433/{database}"
            f"?driver=ODBC+Driver+17+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"
        )
        engine = create_engine(connection_string)
        self.engines[name] = engine

class BigQueryConnector:
    """Google BigQuery connector."""
    
    def __init__(self, project_id: str, credentials_path: str = None):
        self.project_id = project_id
        self.credentials_path = credentials_path
        
    def query(self, sql: str) -> pd.DataFrame:
        """Execute BigQuery SQL and return DataFrame."""
        try:
            import pandas_gbq
            
            return pandas_gbq.read_gbq(
                sql, 
                project_id=self.project_id,
                credentials=self.credentials_path,
                dialect='standard'
            )
            
        except ImportError:
            logger.error("pandas-gbq not installed. Install with: pip install pandas-gbq")
            raise
        except Exception as e:
            logger.error(f"BigQuery query failed: {e}")
            raise