from time import timezone
from fastapi import Depends, HTTPException, status, Query, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from typing import Optional
from app.dependencies.db import get_session
from app.schemas.user import UserResponse
from app.common.user import get_user_by_id

load_dotenv()
# ================= 配置区域 =================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20160

# =============== 密码哈希区域 ================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ============= JWT token 相关函数 =============
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============= OAuth2 依赖定义 ================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), session=Depends(get_session)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        user = get_user_by_id(user_id, session)
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def get_current_user_flexible(
    request: Request,
    token: Optional[str] = Query(None),
    session=Depends(get_session)
) -> UserResponse:
    """
    支持从URL参数或Authorization header中获取token的认证函数
    优先使用Authorization header，如果没有则使用URL参数中的token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 首先尝试从Authorization header获取token
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    elif not token:
        # 如果header和URL参数都没有token，则认证失败
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
        user = get_user_by_id(user_id, session)
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
