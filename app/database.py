from typing import Any, Generator
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# config sqlite
DATABASE_URL = "sqlite:///./app.db"

engine: Engine = create_engine(DATABASE_URL, connect_args={
                               "check_same_thread": False})
SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# dependency to obtain the session in the bank
def get_db() -> Generator[Session, Any, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
