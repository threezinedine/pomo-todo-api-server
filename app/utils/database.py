from sqlalchemy.orm import Session

from databases.models import (
    User,
    Task,
)


def clear_database(session: Session):
    session.query(User).delete()
    session.query(Task).delete()
    session.commit()
