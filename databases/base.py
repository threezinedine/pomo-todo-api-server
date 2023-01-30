import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from dotenv import load_dotenv
from app.constants import (
    DATABASE_URI_ENV_VARIABLE_KEY,
    DATABASE_URI_DEFAULT,
)


load_dotenv()
Base = declarative_base()

from .models.User import User
from .models.Task import Task

engine = create_engine(os.getenv(DATABASE_URI_ENV_VARIABLE_KEY, DATABASE_URI_DEFAULT))
LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    try:
        Base.metadata.create_all(engine)
        session = LocalSession()
        yield session
    finally:
        session.close()
