from pydantic import BaseModel, Field
from typing import Optional


class ChatBase(BaseModel):
    chat_name: str = Field(max_length=64)


class ChatResponse(ChatBase):
    chat_id: str
    user_id: str
    create_time: int
    update_time: int


class ChatCreate(ChatBase):
    user_id: Optional[str] = None  # 这将在API中设置


class ChatUpdate(BaseModel):
    chat_id: str
    chat_name: str = Field(max_length=64)
