from sqlmodel import create_engine, Session
from typing import Generator

DATABASE_URL = "mysql+pymysql://root:Dpj89757!@47.116.194.240:3306/chatbot"

engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
