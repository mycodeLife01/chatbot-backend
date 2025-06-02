from fastapi import Depends

from app.core.security import get_current_user
from app.dependencies.db import get_session

session_dep = Depends(get_session)
current_user_dep = Depends(get_current_user)
