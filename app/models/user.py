from sqlmodel import Field, SQLModel, UniqueConstraint
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ =  'user'
    __table_args__ = (UniqueConstraint("username"))

    user_id: int = Field(primary_key=True)
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)
    avatar: str = Field(nullable=False)
    create_time: int = Field(nullable=False, default_factory=datetime.now(timezone.utc).timestamp())
    update_time: int = Field(nullable=False, default_factory=datetime.now(timezone.utc).timestamp())
    is_delete: int = Field(nullable=False, default=0)