from pydantic import BaseModel, Field
from typing import Literal

class Message(BaseModel):
    id: str
    role: Literal["human", "assistant", "system"] = Field(..., description="The role of the message sender")
    content : str

class ChatHistory(BaseModel):
    thread_id : str
    title : str
