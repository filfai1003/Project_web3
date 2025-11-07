from typing import List, Optional
from pydantic import BaseModel, Field

class Interaction(BaseModel):
	interaction_id: str = Field(..., description="Unique identifier for the interaction")
	chat_id: str = Field(..., description="Unique identifier for the chat session")
	sender: str = Field(..., description="Sender of the message, Username or model, e.g., 'filfai' or 'Llama-2-3B'")
	role: str = Field(..., description="Role of the sender, e.g., 'user' or 'assistant'")
	content: str = Field(..., description="Content of the message")
	datetime: datetime = Field(..., description="Timestamp of the interaction")

class ChatBase(BaseModel):
	chat_id: str = Field(..., description="Unique identifier for the chat session")
	user: str = Field(..., description="Username of the chat participant, e.g., 'filfai'")
	current_model: Optional[str] = Field(None, description="Current model being used for the chat, e.g., 'Llama-2-3B'; può essere null")
	interactions: List[Interaction] = Field(..., description="List of interactions in the chat")