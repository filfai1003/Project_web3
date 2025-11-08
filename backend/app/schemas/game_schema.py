from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class InteractionOut(BaseModel):
    sender: str = Field(..., description="Sender of the interaction: player or ia")
    content: str = Field(..., description="Interaction content")
    created_at: datetime = Field(..., description="Timestamp of the interaction")


class GameOut(BaseModel):
    game_id: str = Field(..., description="Unique identifier for the game")
    owner_id: str = Field(..., description="User ID of the game owner")
    title: str = Field(..., description="Title of the game")
    interactions: List[InteractionOut] = Field(default_factory=list, description="Ordered list of interactions for the game")
    