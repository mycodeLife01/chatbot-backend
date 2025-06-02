import logging
from app.crud.chat_message import (
    find_messages_by_chat_id,
    create_message,
)
from app.crud.chat import find_chat_by_chat_id
from app.schemas.chat_file import ChatFileCreate
from app.schemas.chat_message import ChatMessageResponse, ChatMessageCreate
from app.core.exceptions import ChatDeletedException
from app.service.chat_file import create_files_for_message, get_files_for_message
from typing import Optional, List


def get_messages_by_chat_id(
    chat_id: str, user_id: str, session
) -> list[ChatMessageResponse]:
    try:
        # 验证聊天是否属于当前用户
        chat = find_chat_by_chat_id(chat_id, session)
        if not chat:
            raise ChatDeletedException("Chat not found")
        if chat.is_delete == 1:
            raise ChatDeletedException("Chat has been deleted")
        if chat.user_id != user_id:
            raise ChatDeletedException(
                "Access denied: Chat does not belong to current user"
            )

        messages = find_messages_by_chat_id(chat_id, session)
        result = []
        for m in messages:
            # 使用chat_file service获取文件
            chat_file_responses = get_files_for_message(m.message_id, session)

            # 直接使用对象属性创建响应
            message_response = ChatMessageResponse(
                message_id=m.message_id,
                chat_id=m.chat_id,
                message_content=m.message_content,
                is_ai=m.is_ai,
                create_time=m.create_time,
                files=chat_file_responses,
            )
            result.append(message_response)
        return result
    except ChatDeletedException as e:
        logging.error(
            f"Failed getting messages because chat was deleted or not found: {e}",
            exc_info=True,
        )
        raise
    except Exception as e:
        logging.error(
            f"Error getting messages because of unexpected server error: {e}",
            exc_info=True,
        )
        raise


def add_new_message(
    message_create: ChatMessageCreate,
    user_id: str,
    session,
    files_create: Optional[List[ChatFileCreate]] = None,
) -> ChatMessageResponse:
    try:
        # 验证聊天是否存在且未被删除
        chat = find_chat_by_chat_id(message_create.chat_id, session)
        if not chat:
            raise ChatDeletedException("Chat not found")
        if chat.is_delete == 1:
            raise ChatDeletedException("Chat has been deleted")
        # 验证聊天是否属于当前用户
        if chat.user_id != user_id:
            raise ChatDeletedException(
                "Access denied: Chat does not belong to current user"
            )

        # 创建消息
        new_message = create_message(message_create, session)

        # 使用chat_file service创建文件记录
        chat_file_responses = create_files_for_message(
            new_message.message_id, files_create, session
        )

        # 直接使用对象属性创建响应
        return ChatMessageResponse(
            message_id=new_message.message_id,
            chat_id=new_message.chat_id,
            message_content=new_message.message_content,
            is_ai=new_message.is_ai,
            create_time=new_message.create_time,
            files=chat_file_responses,
        )
    except ChatDeletedException as e:
        logging.error(
            f"Failed adding message because chat was deleted or not found: {e}",
            exc_info=True,
        )
        raise
    except Exception as e:
        logging.error(
            f"Error adding message because of unexpected server error: {e}",
            exc_info=True,
        )
        raise




