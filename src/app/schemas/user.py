from pydantic import BaseModel, EmailStr
import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True
    is_verified: bool = False

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str = None

class UserInDB(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    
    class Config:
        orm_mode = True