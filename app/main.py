from app.core import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.exception_handlers import register_exception_handlers
from app.router.user import router as user_router
from app.router.chat import router as chat_router
from app.router.chat_message import router as message_router


app: FastAPI = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)
register_exception_handlers(app)
