from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class UserOut(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    username: str = Field(..., description="Username")
    email: Optional[EmailStr] = Field(None, description="User email address")
    is_active: bool = Field(True, description="Whether the user is active")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")

