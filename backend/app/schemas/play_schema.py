from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class messageIn(BaseModel):
    game_id: str = Field(..., description="Unique identifier for the game")
    message: str = Field(..., description="Input message from the player")

class messageOut(BaseModel):
    interaction_id: str = Field(..., description="Unique identifier for the interaction")
    sender: str = Field(..., description="Sender of the message: player or ia")
    content: str = Field(..., description="Content of the message")
    created_at: str = Field(..., description="Timestamp of the message creation")
    