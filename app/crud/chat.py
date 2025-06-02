from sqlmodel import Session, select, update
from sqlalchemy import CursorResult
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate
from app.common.time_tools import now_timestamp


def find_chats_by_user_id(user_id: str, session: Session) -> list[Chat]:
    stmt = select(Chat).where(Chat.user_id == user_id, Chat.is_delete == 0)
    chats = session.exec(stmt).all()
    return chats


def find_chat_by_chat_id(chat_id: str, session: Session) -> Chat:
    stmt = select(Chat).where(Chat.chat_id == chat_id, Chat.is_delete == 0)
    chat = session.exec(stmt).one_or_none()
    return chat


def create_chat(chat_create: ChatCreate, session: Session) -> Chat:
    new_chat = Chat(**chat_create.model_dump())
    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)
    return new_chat


def find_chat_by_chat_name(chat_name: str, session: Session) -> Chat:
    stmt = select(Chat).where(Chat.chat_name == chat_name, Chat.is_delete == 0)
    chat = session.exec(stmt).one_or_none()
    return chat


def delete_chat(chat_id: str, session: Session) -> int:
    stmt = update(Chat).where(Chat.chat_id == chat_id).values(is_delete=1)
    result: CursorResult = session.exec(stmt)
    session.commit()
    return result.rowcount


def update_chat(chat_update: ChatUpdate, session: Session) -> int:
    stmt = (
        update(Chat)
        .where(Chat.chat_id == chat_update.chat_id, Chat.is_delete == 0)
        .values(chat_name=chat_update.chat_name, update_time=now_timestamp())
    )
    result: CursorResult = session.exec(stmt)
    session.commit()
    return result.rowcount
