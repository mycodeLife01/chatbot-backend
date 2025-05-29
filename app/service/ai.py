from dotenv import load_dotenv
from openai import OpenAI
import os

from app.crud.chat_message import create_message, find_messages_by_chat_id
from app.schemas.chat_message import ChatMessageCreate
from app.schemas.user_record import UserRecord

load_dotenv()


def get_ai_response(messages: list[UserRecord]) -> str:
    base_message = {
        "role": "system",
        "content": "你是一个热情的AI助手，擅长回答用户的问题。",
    }
    client = OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
    )

    # 将UserRecord对象转换为字典格式
    message_dicts = [{"role": msg.role, "content": msg.content} for msg in messages]
    
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[base_message, *message_dicts],
    )
    return completion.choices[0].message.content


def do_ai_response(message: str, chat_id: str, session) -> str:
    chat_messages = find_messages_by_chat_id(chat_id, session)
    user_records = [
        UserRecord(
            role="user" if message.is_ai == 0 else "assistant",
            content=message.message_content,
        )
        for message in chat_messages
    ]
    user_records.append(UserRecord(role="user", content=message))
    ai_response = get_ai_response(user_records)
    create_message(
        ChatMessageCreate(
            chat_id=chat_id,
            message_content=ai_response,
            is_ai=1,
        ),
        session,
    )
    return ai_response
