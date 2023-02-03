from sqlalchemy import (
    Column,
    Integer,
    String,
)
from constants.database.user import (
    USER_TABLE_NAME,
    USERNAME_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    USER_DESCRIPTION_MAX_LENGTH,
    IMAGE_PATH_MAX_LENGTH,
)

from databases.base import Base


class User(Base):
    __tablename__ = USER_TABLE_NAME

    userId = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=USERNAME_MAX_LENGTH), unique=True)
    password = Column(String(length=PASSWORD_MAX_LENGTH))
    description = Column(String(length=USER_DESCRIPTION_MAX_LENGTH), nullable=True)
    imagePath = Column(String(length=IMAGE_PATH_MAX_LENGTH), nullable=True)

    def __init__(self, username: str, 
                    password: str, 
                    description: str = None,
                    imagePath: str = None):
        self.username = username
        self.password = password
        self.description = description
        self.imagePath

    def match_password(self, password: str):
        return self.password == password

    def __repr__(self):
        return f"<User userId={self.userId} username={self.username} />"
