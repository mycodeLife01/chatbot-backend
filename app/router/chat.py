from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.dependencies.db import get_session
from app.schemas.user import UserResponse
from app.schemas.chat import ChatCreate, ChatUpdate, ChatResponse
from app.service.chat import (
    get_all_chats,
    add_new_chat,
    update_user_chat,
    delete_user_chat,
)
from app.dependencies.common import session_dep, current_user_dep

router = APIRouter(prefix="/chats", tags=["Chat"])


@router.get("/all")
def all_chats(current_user: UserResponse = current_user_dep, session=session_dep):
    return get_all_chats(current_user.user_id, session)


@router.post("/new", response_model=ChatResponse)
def create_new_chat(
    chat_create: ChatCreate,
    current_user: UserResponse = current_user_dep,
    session=session_dep,
):
    # 确保chat归属于当前用户
    chat_create.user_id = current_user.user_id
    return add_new_chat(chat_create, session)


@router.put("/update")
def update_chat(
    chat_update: ChatUpdate,
    current_user: UserResponse = current_user_dep,
    session=session_dep,
):
    rows_affected = update_user_chat(chat_update, session)
    return {"success": True, "rows_affected": rows_affected}


@router.delete("/remove/{chat_id}")
def remove_chat(
    chat_id: str, current_user: UserResponse = current_user_dep, session=session_dep
):
    rows_affected = delete_user_chat(chat_id, session)
    return {"success": True, "rows_affected": rows_affected}
