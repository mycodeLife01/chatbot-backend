from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user
from app.service.user import user_login, user_register
from app.schemas.user import UserCreate, Token, UserLogin, UserResponse
from app.dependencies.db import get_session
from app.dependencies.common import session_dep

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post("/register", response_model=Token)
def register(user_create: UserCreate, session=session_dep):
    return user_register(user_create, session)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session=session_dep):
    return user_login(
        UserLogin(username=form_data.username, password=form_data.password), session
    )
