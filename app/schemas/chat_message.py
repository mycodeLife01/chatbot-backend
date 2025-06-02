from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.chat_file import ChatFileResponse


class ChatMessageBase(BaseModel):
    chat_id: str
    message_content: str
    is_ai: int


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageResponse(ChatMessageBase):
    message_id: str
    create_time: int
    files: Optional[list[ChatFileResponse]] = Field(default=None, max_length=5)
    is_complete: bool = Field(default=False)