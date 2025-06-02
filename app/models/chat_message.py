from sqlmodel import SQLModel, Field
import uuid
from app.common.time_tools import now_timestamp


class ChatMessage(SQLModel, table=True):
    __tablename__ = 'message'
    message_id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    message_content: str = Field(nullable=False)
    chat_id: str = Field(foreign_key="chat.chat_id")
    create_time: int = Field(nullable=False, default_factory=now_timestamp)
    update_time: int = Field(nullable=False, default_factory=now_timestamp)
    is_ai: int = Field(nullable=False, default=0)
    is_complete: int = Field(nullable=False, default=0)
