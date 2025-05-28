from sqlmodel import Session, select
from app.models.chat_file import ChatFile
from app.schemas.chat_file import ChatFileCreate
from app.common.time_tools import now_timestamp


def create_file_by_message_id(
    chat_file_create: ChatFileCreate, session: Session
) -> ChatFile:
    new_file = ChatFile(
        file_name=chat_file_create.file_name,
        file_size=chat_file_create.file_size,
        file_type=chat_file_create.file_type,
        file_url=chat_file_create.file_url,
        message_id=chat_file_create.message_id,
        is_ai=chat_file_create.is_ai,
        create_time=now_timestamp(),
    )
    session.add(new_file)
    session.commit()
    session.refresh(new_file)
    return new_file


def find_files_by_message_id(message_id: str, session: Session) -> list[ChatFile]:
    stmt = select(ChatFile).where(ChatFile.message_id == message_id)
    files = session.exec(stmt).all()
    return files
