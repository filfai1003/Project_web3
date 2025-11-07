from pydantic import BaseModel, Field


class GameOut(BaseModel):
    game_id: str = Field(..., description="Unique identifier for the game")
    owner_id: str = Field(..., description="User ID of the game owner")
    title: str = Field(..., description="Title of the game")
    