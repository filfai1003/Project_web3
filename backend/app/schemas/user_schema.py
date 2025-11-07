from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., description="Username, e.g., 'filfai'")
    email: Optional[EmailStr] = Field(None, description="User email address")


class UserCreate(UserBase):
    password: str = Field(..., description="Plain-text password for signup")


class UserOut(UserBase):
    user_id: str = Field(..., description="Unique identifier for the user")
    is_active: bool = Field(True, description="Whether the user is active")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None
