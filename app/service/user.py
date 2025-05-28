from app.core.exceptions import (
    UserExistException,
    UserNotExistException,
    UserPasswordInvalidException,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.crud.user import create_user, find_user_by_id, find_user_by_username
from app.schemas.user import UserCreate, UserLogin, UserResponse
import logging
from app.schemas.user import Token


def user_register(user_create: UserCreate, session) -> Token:
    try:
        user_db = find_user_by_username(user_create.username, session)
        if user_db:
            raise UserExistException()
        user_create.password = hash_password(user_create.password)
        new_user = create_user(user_create, session)
        access_token = create_access_token({"sub": new_user.user_id})
        return Token(access_token=access_token)
    except UserExistException as e:
        logging.error(
            f"Failed registering a new user because it has existed: {e}",
            exc_info=True,
        )
        raise
    except Exception as e:
        logging.error(
            f"Error while registering a new user because of an unexpected system error:{e}",
            exc_info=True,
        )
        raise


def user_login(user_login: UserLogin, session) -> Token:
    try:
        user = find_user_by_username(user_login.username, session)
        if not user:
            raise UserNotExistException()
        if not verify_password(user_login.password, user.password):
            raise UserPasswordInvalidException()
        access_token = create_access_token({"sub": user.user_id})
        return Token(access_token=access_token)
    except UserNotExistException as e:
        logging.error(
            f"Failed logining user because it does not exist: {e}",
            exc_info=True,
        )
        raise
    except UserPasswordInvalidException as e:
        logging.error(
            f"Failed logining user because of a invalid password: {e}",
            exc_info=True,
        )
        raise
    except Exception as e:
        logging.error(
            f"Error while logining user because of an unexpected system error:{e}",
            exc_info=True,
        )
        raise