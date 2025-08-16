from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    username: Optional[str] = None
    
class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    
class UserInDB(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    
class User(UserInDB):
    pass

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime
    is_active: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


