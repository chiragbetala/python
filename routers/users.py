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
        query = text("SELECT * FROM app.m_user")
        result = await session.execute(query)
        users = [dict(row._mapping) for row in result]
        return users
    except Exception as e:
        print(f"Error fetching users: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

@router.get("/user-roles", response_model=List[Dict])
async def get_user_roles(session: AsyncSession = Depends(get_session)):
    try:
        query = text("SELECT * FROM app.m_role")  # Adjust table name as per your schema
        result = await session.execute(query)
        roles = [dict(row._mapping) for row in result]
        return roles
    except Exception as e:
        print(f"Error fetching user roles: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
