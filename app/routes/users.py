from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import UserCreate, UserUpdate, UserOut
from app.db import create_user, get_user_by_id, get_users, update_user, delete_user

router = APIRouter()

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate):
    """Create a new user."""
    try:
        db_user = await create_user(user)
        return UserOut.from_orm(db_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/users", response_model=List[UserOut])
async def list_users(skip: int = 0, limit: int = 10):
    """List users with pagination."""
    db_users = await get_users(skip=skip, limit=limit)
    return [UserOut.from_orm(user) for user in db_users]

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    """Get a user by ID."""
    db_user = await get_user_by_id(user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.from_orm(db_user)

@router.put("/users/{user_id}", response_model=UserOut)
async def update_user_endpoint(user_id: str, user_update: UserUpdate):
    """Update a user by ID."""
    try:
        db_user = await update_user(user_id, user_update)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserOut.from_orm(db_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(user_id: str):
    """Delete a user by ID."""
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")