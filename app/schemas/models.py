from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from bson import ObjectId

# Custom type for ObjectId to handle MongoDB ObjectId in Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Input model for creating a user
class UserCreate(BaseModel):
    email: EmailStr
    name: str

# Input model for updating a user (partial update allowed)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None

# Output model for user responses
class UserOut(BaseModel):
    id: str
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        orm_mode = True  # Allows conversion from ORM objects or dicts

# Internal model for database operations (includes ObjectId)
class UserDB(BaseModel):
    id: PyObjectId
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}