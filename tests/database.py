from os import getenv
from sqlalchemy.orm import (
    sessionmaker,
)
from sqlalchemy.engine import (
    create_engine,
)

from databases.base import Base
from constants.env import (
    TEST_DATABASE_URI_ENV_VARIABLE_KEY,
    TEST_DATABASE_URI_DEFAULT,
)

engine = create_engine(getenv(TEST_DATABASE_URI_ENV_VARIABLE_KEY, TEST_DATABASE_URI_DEFAULT))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_testing_session():
    try:
        Base.metadata.create_all(engine) 
        session = SessionLocal()
        yield session
    finally:
        session.close()
