from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from app.config import settings
from app.models import UserDB, UserCreate, UserUpdate

# Global MongoDB client and database
client: AsyncIOMotorClient = None
db = None

async def connect_to_mongo():
    """Connect to MongoDB on app startup."""
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    # Create indexes
    await db.users.create_index("email", unique=True)
    print("Connected to MongoDB")

async def close_mongo_connection():
    """Close MongoDB connection on app shutdown."""
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")

# Helper functions for User CRUD operations

async def create_user(user_data: UserCreate) -> UserDB:
    """Create a new user in the database."""
    user_dict = user_data.dict()
    user_dict["created_at"] = datetime.utcnow()
    try:
        result = await db.users.insert_one(user_dict)
        user_dict["id"] = result.inserted_id
        return UserDB(**user_dict)
    except DuplicateKeyError:
        raise ValueError("Email already exists")

async def get_user_by_id(user_id: str) -> Optional[UserDB]:
    """Get a user by ID."""
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = user.pop("_id")
        return UserDB(**user)
    return None

async def get_users(skip: int = 0, limit: int = 10) -> List[UserDB]:
    """Get a list of users with pagination."""
    users = []
    cursor = db.users.find().skip(skip).limit(limit)
    async for user in cursor:
        user["id"] = user.pop("_id")
        users.append(UserDB(**user))
    return users

async def update_user(user_id: str, update_data: UserUpdate) -> Optional[UserDB]:
    """Update a user by ID."""
    update_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_dict:
        return await get_user_by_id(user_id)
    try:
        result = await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
        if result.modified_count:
            return await get_user_by_id(user_id)
        return None
    except DuplicateKeyError:
        raise ValueError("Email already exists")

async def delete_user(user_id: str) -> bool:
    """Delete a user by ID."""
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0