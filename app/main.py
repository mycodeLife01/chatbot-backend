from app.core import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.exception_handlers import register_exception_handlers
from app.router.user import router as user_router
from app.router.chat import router as chat_router
from app.router.chat_message import router as message_router


app: FastAPI = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://localhost:4173", "http://127.0.0.1:4173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)
register_exception_handlers(app)
