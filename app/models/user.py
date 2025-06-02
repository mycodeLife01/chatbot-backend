from sqlmodel import Field, SQLModel, UniqueConstraint
from app.common.time_tools import now_timestamp
import uuid


class User(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("username"),
        UniqueConstraint("email"),
    )
    user_id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    username: str = Field(nullable=False, max_length=32)
    password: str = Field(nullable=False, max_length=255)
    avatar: str = Field(nullable=False, max_length=255)
    create_time: int = Field(nullable=False, default_factory=now_timestamp)
    update_time: int = Field(nullable=False, default_factory=now_timestamp)
    is_delete: int = Field(nullable=False, default=0)
    email: str = Field(max_length=64)
