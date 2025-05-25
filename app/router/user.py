from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from core.security import get_current_user
from service.user import user_login, user_register
from schemas.user import UserCreate, Token, UserLogin, UserResponse
from dependencies.db import get_session

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

session_dep = Depends(get_session)


@router.post("/register", response_model=Token)
def register(user_create: UserCreate, session=session_dep):
    return user_register(user_create, session)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session=session_dep):
    return user_login(
        UserLogin(username=form_data.username, password=form_data.password), session
    )


@router.get("/chats")
def chats(current_user: UserResponse = Depends(get_current_user)):
    if current_user:
        return {"user": current_user.username, "chats": ["nihao", "hello"]}
    return {"not login"}
