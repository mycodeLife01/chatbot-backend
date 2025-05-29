from pydantic import BaseModel


class UserRecord(BaseModel):
    role: str
    content: str