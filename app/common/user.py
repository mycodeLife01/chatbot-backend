from schemas.user import UserResponse
from crud.user import find_user_by_id


def get_user_by_id(id: str, session) -> UserResponse | None:
    user = find_user_by_id(id, session)
    if user:
        return UserResponse(**user.model_dump())
    return None
