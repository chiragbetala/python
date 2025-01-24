# create_async_engine: Creates an async engine to interact with the database.
# AsyncSession: Represents a session for database operations in an asynchronous context.
# async_sessionmaker: Creates a factory for producing asynchronous session objects.
# declarative_base: Provides a base class for defining database models (ORM mappings).
# os: Used to fetch environment variables for database configuration.
# AsyncGenerator: Provides type hinting for generator-based async functions, like get_session.

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os


# Database URL mapping
DB_URLS = {
    'pg': 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}',
    'mysql': 'mysql+aiomysql://{user}:{password}@{host}:{port}/{database}',
    'sqlite': 'sqlite+aiosqlite:///{database}'
}

# Get database configuration from environment
DB_TYPE = os.getenv('DB_TYPE')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
DB_SEARCH_PATH = os.getenv('DB_SEARCH_PATH')

# Create database URL
if not DB_TYPE:
    raise ValueError("DB_TYPE environment variable is not set")

if DB_TYPE == 'sqlite':
    DATABASE_URL = DB_URLS[DB_TYPE].format(database=DB_NAME)
else:
    DATABASE_URL = DB_URLS[DB_TYPE].format(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Disable SQL query logging (set True for debugging)
    pool_pre_ping=True, # Check connection validity before using , Ensures dead connections are not used.
    pool_size=5, # Number of connections in the connection pool
    max_overflow=5,  # Extra connections allowed when the pool is full
    connect_args={'server_settings': {'search_path': DB_SEARCH_PATH}} if DB_TYPE == 'pg' else {}
)

# Create session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create declarative base for models
Base = declarative_base()

# Session management
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Database initialization
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Database cleanup
async def close_db():
    await engine.dispose()
