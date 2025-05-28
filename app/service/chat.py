import logging
from app.core.exceptions import ChatDeletedException, ChatExistException
from app.crud.chat import (
    create_chat,
    delete_chat,
    find_chat_by_chat_id,
    find_chat_by_chat_name,
    find_chats_by_user_id,
    update_chat,
)
from app.schemas.chat import ChatCreate, ChatResponse, ChatUpdate


def get_all_chats(user_id, session) -> list[ChatResponse]:
    chats = find_chats_by_user_id(user_id, session)
    return [ChatResponse(**c.model_dump()) for c in chats]


def add_new_chat(chat_create: ChatCreate, session) -> ChatResponse:
    try:
        # 检查该用户是否已有同名聊天
        existing_chats = find_chats_by_user_id(chat_create.user_id, session)
        for chat in existing_chats:
            if chat.chat_name == chat_create.chat_name:
                raise ChatExistException("Chat with this name already exists for user")

        new_chat = create_chat(chat_create, session)
        return ChatResponse(**new_chat.model_dump())
    except ChatExistException as e:
        logging.error(
            f"Failed adding a new chat because it already exists: {e}", exc_info=True
        )
        raise
    except Exception as e:
        logging.error(
            f"Error adding a new chat because of an unexpected server error: {e}",
            exc_info=True,
        )
        raise


def delete_user_chat(chat_id: str, session) -> int:
    try:
        chat = find_chat_by_chat_id(chat_id, session)
        if not chat:
            raise ChatDeletedException("Chat not found")
        if chat.is_delete == 1:
            raise ChatDeletedException("Chat already deleted")
        return delete_chat(chat_id, session)
    except ChatDeletedException as e:
        logging.error(
            f"Failed deleting a chat because it was already deleted: {e}", exc_info=True
        )
        raise
    except Exception as e:
        logging.error(
            f"Error deleting chat because of unexpected server error: {e}",
            exc_info=True,
        )
        raise


def update_user_chat(chat_update: ChatUpdate, session) -> int:
    try:
        chat = find_chat_by_chat_id(chat_update.chat_id, session)
        if not chat:
            raise ChatDeletedException("Chat not found")
        if chat.is_delete == 1:
            raise ChatDeletedException("Chat has been deleted")
        return update_chat(chat_update, session)
    except ChatDeletedException as e:
        logging.error(
            f"Failed updating chat because it was deleted or not found: {e}",
            exc_info=True,
        )
        raise
    except Exception as e:
        logging.error(
            f"Error updating chat because of unexpected server error: {e}",
            exc_info=True,
        )
        raise
