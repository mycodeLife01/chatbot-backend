import logging
from typing import Optional, List
from app.crud.chat_file import create_file_by_message_id, find_files_by_message_id
from app.schemas.chat_file import ChatFileCreate, ChatFileResponse


def create_files_for_message(
    message_id: str, 
    files_create: Optional[List[ChatFileCreate]], 
    session
) -> List[ChatFileResponse]:
    """为消息创建文件记录"""
    chat_file_responses = []
    if files_create:
        for file_create in files_create:
            file_create.message_id = message_id
            file_obj = create_file_by_message_id(file_create, session)
            # 直接使用属性创建响应对象
            chat_file_responses.append(ChatFileResponse(
                file_id=file_obj.file_id,
                file_name=file_obj.file_name,
                file_size=file_obj.file_size,
                file_type=file_obj.file_type,
                is_ai=file_obj.is_ai,
                message_id=file_obj.message_id,
                file_url=file_obj.file_url
            ))
    return chat_file_responses


def get_files_for_message(message_id: str, session) -> List[ChatFileResponse]:
    """获取消息的所有文件"""
    files = find_files_by_message_id(message_id, session)
    chat_file_responses = []
    for file in files:
        chat_file_responses.append(ChatFileResponse(
            file_id=file.file_id,
            file_name=file.file_name,
            file_size=file.file_size,
            file_type=file.file_type,
            is_ai=file.is_ai,
            message_id=file.message_id,
            file_url=file.file_url
        ))
    return chat_file_responses 