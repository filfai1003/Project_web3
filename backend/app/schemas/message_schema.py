from pydantic import BaseModel, Field

class MessageIn(BaseModel):
    user: str = Field(..., description="Username of the message sender, e.g., 'filfai'")
    chat_id: str = Field(..., description="Unique identifier for the chat session")
    content: str = Field(..., description="Content of the message")

class MessageOut(BaseModel):
    message_id: str = Field(..., description="Unique identifier for the message")
    user: str = Field(..., description="Username of the message sender, e.g., 'filfai'")
    chat_id: str = Field(..., description="Unique identifier for the chat session")
    content: str = Field(..., description="Content of the message")
    timestamp: str = Field(..., description="Timestamp when the message was created")
