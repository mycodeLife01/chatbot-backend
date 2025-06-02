from pydantic import BaseModel
from typing import Optional


class ChatFileBase(BaseModel):
    file_name: str
    file_size: int
    file_type: int
    is_ai: int


class ChatFileCreate(BaseModel):
    message_id: Optional[str] = None
    file_name: str
    file_size: int
    file_type: int
    is_ai: int
    file_url: Optional[str] = None


class ChatFileResponse(ChatFileBase):
    file_id: str
    message_id: str
    file_url: str
