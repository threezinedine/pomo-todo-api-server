import os
from sqlalchemy.orm import Session

from databases.models import (
    User,
    Task,
)
from constants import IMAGE_BASE_FOLDER


def clear_database(session: Session):
    session.query(User).delete()
    session.query(Task).delete()
    session.commit()


def create_the_saved_image_path(image_name: str):
    return os.path.join(IMAGE_BASE_FOLDER, f"{image_name}.png")
