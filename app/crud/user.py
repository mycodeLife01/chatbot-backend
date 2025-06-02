from sqlalchemy import CursorResult
from app.dependencies.db import get_session
from sqlmodel import Session
from app.schemas.user import UserCreate, UserUpdate
from fastapi import Depends
from app.models.user import User
from sqlmodel import update, select


def create_user(user_create: UserCreate, session: Session) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    session.commit()
    return user


def delete_user(user_id: str, session: Session) -> int:
    stmt = update(User).where(User.user_id == user_id).values(is_delete=1)
    result: CursorResult = session.exec(stmt)
    session.commit()
    return result.rowcount


def update_user(user_update: UserUpdate, session: Session) -> int:
    stmt = (
        update(User)
        .where(User.user_id == user_update.user_id)
        .values(**user_update.model_dump())
    )
    result: CursorResult = session.exec(stmt)
    session.commit()
    return result.rowcount


def find_user_by_id(user_id: str, session: Session) -> User | None:
    stmt = select(User).where(User.user_id == user_id, User.is_delete==0)
    user: User = session.exec(stmt).one_or_none()
    return user


def find_users_by_ids(user_ids: list[str], session: Session) -> list[User]:
    stmt = select(User).where(User.user_id.in_(user_ids), User.is_delete==0)
    users: list[User] = session.exec(stmt).all()
    return users


def find_user_by_username(username: str, session: Session) -> User | None:
    stmt = select(User).where(User.username == username, User.is_delete==0)
    user: User = session.exec(stmt).one_or_none()
    return user
