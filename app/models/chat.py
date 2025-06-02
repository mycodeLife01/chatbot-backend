import uuid
from sqlmodel import Field, SQLModel
from app.common.time_tools import now_timestamp


class Chat(SQLModel, table=True):
    chat_id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    chat_name: str = Field(nullable=False)
    user_id: str = Field(foreign_key="user.user_id")
    create_time: int = Field(nullable=False, default_factory=now_timestamp)
    update_time: int = Field(nullable=False, default_factory=now_timestamp)
    is_delete: int = Field(nullable=False, default=0)
