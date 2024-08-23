# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
import datetime
import uuid

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., max_length=255)  # New name field
    is_active: bool = True
    is_verified: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(UserBase):
    password: str = Field(None, min_length=8, max_length=128)

class UserInDBBase(UserBase):
    id: uuid.UUID
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True

class UserInDB(UserInDBBase):
    hashed_password: str

class UserOut(UserInDBBase):
    pass
