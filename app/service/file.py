import os
import uuid
from fastapi import HTTPException, UploadFile

from app.schemas.chat_file import ChatFileCreate

# 文件配置
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".gif"}


def get_file_type(filename: str) -> int:
    """根据文件扩展名返回文件类型"""
    ext = os.path.splitext(filename)[1].lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif"}:
        return 1  # 图片
    elif ext in {".txt", ".pdf", ".doc", ".docx"}:
        return 2  # 文档
    else:
        return 3  # 其他


async def save_file(files: list[UploadFile]) -> list[ChatFileCreate]:
    # 处理文件上传
    files_create = []
    if files:
        # 检查文件数量限制
        if len(files) > 5:
            raise HTTPException(status_code=400, detail="最多只能上传5个文件")

        # 确保上传目录存在
        upload_dir = "static/chatfiles"
        os.makedirs(upload_dir, exist_ok=True)

        for file in files:
            if file.filename:
                # 检查文件扩展名
                file_extension = os.path.splitext(file.filename)[1].lower()
                if file_extension not in ALLOWED_EXTENSIONS:
                    raise HTTPException(
                        status_code=400, detail=f"不支持的文件类型: {file_extension}"
                    )

                # 读取文件内容
                content = await file.read()

                # 检查文件大小
                if len(content) > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"文件 {file.filename} 超过最大大小限制 (10MB)",
                    )

                # 生成唯一文件名
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)

                # 保存文件到磁盘
                try:
                    with open(file_path, "wb") as buffer:
                        buffer.write(content)
                except Exception as e:
                    raise HTTPException(
                        status_code=500, detail=f"文件保存失败: {str(e)}"
                    )

                # 创建文件记录
                file_create = ChatFileCreate(
                    file_name=file.filename,
                    file_size=len(content),
                    file_type=get_file_type(file.filename),
                    is_ai=0,
                    file_url=file_path,
                )
                files_create.append(file_create)
    return files_create
