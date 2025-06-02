from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(max_length=32, min_length=4)
    email: EmailStr = Field(default="123@456.com", max_length=255)


class UserCreate(UserBase):
    avatar: str = Field(default="/static/images/avatar.svg")
    password: str = Field(max_length=32, min_length=4)
    repeat_password: str = Field(max_length=32, min_length=4)

class UserUpdate(UserBase):
    user_id: str
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(UserBase):
    user_id: str
    avatar: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
