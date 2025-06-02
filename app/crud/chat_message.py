from sqlmodel import Session, select, update
from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate
from app.common.time_tools import now_timestamp


def find_messages_by_chat_id(chat_id: str, session: Session) -> list[ChatMessage]:
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.create_time)
    )
    messages = session.exec(stmt).all()
    return messages


def create_message(message_create: ChatMessageCreate, session: Session) -> ChatMessage:
    # 创建消息时不包含files，files需要单独处理
    message_data = message_create.model_dump(exclude={"files"})
    # 确保时间戳字段被正确设置
    current_time = now_timestamp()
    message_data["create_time"] = current_time
    message_data["update_time"] = current_time

    new_message = ChatMessage(**message_data)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message


def find_latest_message_by_chat_id(chat_id: str, session: Session) -> ChatMessage:
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.create_time.desc())
        .limit(1)
    )
    message = session.exec(stmt).first()
    return message

def update_message_content(message_id: str, content: str, session: Session):
    stmt = (
        update(ChatMessage)
        .where(ChatMessage.message_id == message_id)
        .values(message_content=content)
    )
    session.exec(stmt)
    session.commit()

def update_message_is_complete(message_id: str, is_complete: int, session: Session):
    stmt = (
        update(ChatMessage)
        .where(ChatMessage.message_id == message_id)
        .values(is_complete=is_complete)
    )
    session.exec(stmt)
    session.commit()