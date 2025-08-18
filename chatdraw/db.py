import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import dotenv
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Integer, String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


dotenv.load_dotenv()

DB_DRIVERNAME="postgresql+psycopg2"
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_NAME = os.environ["DB_NAME"]

DATABASE_URL = URL.create(DB_DRIVERNAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)


class Base(DeclarativeBase):
    pass


class Sketch(Base):
    __tablename__ = "sketch"

    sketch_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    concept: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    model_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    
    db_session = scoped_session(sessionmaker(
        bind=engine, autocommit=False, autoflush=True, class_=Session
    ))
    yield db_session
    db_session.close()


