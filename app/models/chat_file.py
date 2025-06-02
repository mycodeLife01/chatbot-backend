from sqlmodel import SQLModel, Field
from app.common.time_tools import now_timestamp
import uuid


class ChatFile(SQLModel, table=True):
    __tablename__='file'
    file_id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    file_name: str = Field(nullable=False)
    file_size: int = Field(nullable=False)
    file_url: str = Field(nullable=False)
    message_id: str = Field(foreign_key="message.message_id")
    is_ai: int = Field(nullable=False)
    create_time: int = Field(nullable=False, default_factory=now_timestamp)
    file_type: int = Field(nullable=False)
