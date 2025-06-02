from fastapi import APIRouter, File, UploadFile, Form, Query, Request, Depends
from fastapi.responses import StreamingResponse
from app.dependencies.common import session_dep, current_user_dep
from app.core.security import get_current_user_flexible
from app.service.chat_message import (
    get_messages_by_chat_id,
    add_new_message,
)
from app.schemas.chat_message import ChatMessageCreate, ChatMessageResponse
from app.schemas.user import UserResponse
from typing import Optional, List
from app.service.ai import do_ai_response
from app.service.file import save_file

router = APIRouter(prefix="/messages", tags=["Message"])


@router.get("/")
def messages(
    chat_id: str, current_user: UserResponse = current_user_dep, session=session_dep
):
    return get_messages_by_chat_id(chat_id, current_user.user_id, session)


@router.post("/add", response_model=ChatMessageResponse)
async def create_message(
    chat_id: str = Form(...),
    message_content: str = Form(...),
    is_ai: int = Form(0),
    files: Optional[List[UploadFile]] = File(None),
    current_user: UserResponse = current_user_dep,
    session=session_dep,
):
    # 创建消息对象
    message_create = ChatMessageCreate(
        chat_id=chat_id, message_content=message_content, is_ai=is_ai
    )

    # 处理文件上传
    files_create = await save_file(files)
    return add_new_message(message_create, current_user.user_id, session, files_create)


@router.get("/ai-response")
def generate_response(
    request: Request,
    chat_id: str,
    session=session_dep,
    current_user: UserResponse = Depends(get_current_user_flexible),
):
    return StreamingResponse(
        do_ai_response(chat_id, session),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control",
        }
    )
