from core import logger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.exception_handlers import register_exception_handlers
from router.user import router as user_router

app: FastAPI = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
app.include_router(user_router)
register_exception_handlers(app)