#APIRouter is a FastAPI utility that helps organize your API into multiple modular and reusable routes. It allows you to define routes in separate files and then include them in the main FastAPI app.
#The text function in SQLAlchemy is used to execute raw SQL queries. It wraps a raw SQL string into an SQLAlchemy object that can be executed with a session.
# APIRouter organizes the routes.
# Depends injects reusable dependencies like the database session.
# AsyncSession ensures efficient, non-blocking database operations.
# text allows raw SQL execution when needed.
# HTTPException handles errors gracefully.
# get_session provides a clean and consistent way to manage database sessions.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Dict, List
from db_config import get_session

router = APIRouter(
    prefix="", # Base URL prefix for this router
    tags=["users"] # Swagger/OpenAPI documentation tags
)

@router.get("/users", response_model=List[Dict])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    try:
        #The text() function takes a raw SQL string and converts it into an object that SQLAlchemy can execute.
        query = text("SELECT * FROM m_user")
        result = await session.execute(query)
        # dict(row._mapping): Converts each row into a Python dictionary.
        # row._mapping is a dictionary that contains the column names and values of the current row.
        users = [dict(row._mapping) for row in result]
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

