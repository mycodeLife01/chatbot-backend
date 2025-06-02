from dotenv import load_dotenv
from openai import OpenAI
import os
import logging
from app.crud.chat_message import (
    create_message,
    find_latest_message_by_chat_id,
    find_messages_by_chat_id,
    update_message_content,
    update_message_is_complete,
)
from app.schemas.chat_message import ChatMessageCreate
from app.schemas.user_record import UserRecord
import json
import asyncio

load_dotenv()


def get_ai_response_stream(messages: list[UserRecord]):
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

    # completion = client.chat.completions.create(
    #     model="qwen-plus",
    #     messages=[base_message, *message_dicts],
    #     stream=True,
    # )
    # return completion.choices[0].message.content
    stream = client.chat.completions.create(
        model="qwen-plus",
        messages=[base_message, *message_dicts],
        stream=True,
    )
    return stream


async def do_ai_response(chat_id: str, session):
    try:
        # 获取聊天历史
        chat_messages = find_messages_by_chat_id(chat_id, session)
        user_records = [
            UserRecord(
                role="user" if message.is_ai == 0 else "assistant",
                content=message.message_content,
            )
            for message in chat_messages
        ]
        # 获取最新用户消息
        latest_message = find_latest_message_by_chat_id(chat_id, session)
        user_records.append(
            UserRecord(role="user", content=latest_message.message_content)
        )
        ai_response_stream = get_ai_response_stream(user_records)
        # 创建AI消息记录
        message_id = None
        full_response = ""
        # 逐步处理每个chunk
        for chunk in ai_response_stream:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
            # 第一个chunk时创建消息
            if message_id is None:
                new_message = create_message(
                    ChatMessageCreate(
                        chat_id=chat_id,
                        message_content=full_response,
                        is_ai=1,
                    ),
                    session,
                )
                message_id = new_message.message_id
            else:
                # 更新消息内容
                update_message_content(message_id, full_response, session)
            # 发送数据块到前端
            data = {
                "type": "chunk",
                "content": content,
                "message_id": message_id,
                "full_content": full_response,
            }
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
            # 模拟实时效果
            await asyncio.sleep(0.01)
        # 标记完成
        if message_id:
            update_message_is_complete(message_id, 1, session)
        # 发送完成信号
        final_data = {
            "type": "done",
            "message_id": message_id,
            "full_content": full_response,
        }
        yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
    except Exception as e:
        logging.error(
            f"Error generating AI response because of unexpected server error: {e}",
            exc_info=True,
        )
        error_data = {"type": "error", "message": str(e)}
        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
