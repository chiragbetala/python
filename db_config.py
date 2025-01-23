from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Database URL mapping
DB_URLS = {
    'pg': 'postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}',
    'mysql': 'mysql+aiomysql://{user}:{password}@{host}:{port}/{database}',
    'sqlite': 'sqlite+aiosqlite:///{database}'
}

# Get database configuration from environment
DB_TYPE = os.getenv('DB_TYPE', 'pg').lower()
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_SEARCH_PATH = os.getenv('DB_SEARCH_PATH', 'public')

# Create database URL
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
    echo=False,  # Set to True for SQL logging
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
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
from typing import AsyncGenerator
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
