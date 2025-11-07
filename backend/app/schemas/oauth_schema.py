from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class SignUpIn(BaseModel):
    username: str = Field(..., description="Username, e.g., 'filfai'")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Plain-text password for signup")

class LoginIn(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

class Token(BaseModel):
    access_token: str