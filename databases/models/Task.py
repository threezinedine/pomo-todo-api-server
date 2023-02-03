from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Date,
)
from datetime import datetime

from databases.base import Base
from constants.database.task import (
    TASK_TABLE_NAME,
    TASK_NAME_MAX_LENGTH,
    TASK_DESCRIPTION_MAX_LENGTH,
)


class Task(Base):
    __tablename__ = TASK_TABLE_NAME

    taskId = Column(Integer, primary_key=True, autoincrement=True)
    taskName = Column(String(TASK_NAME_MAX_LENGTH), nullable=False)
    taskDescription = Column(String(TASK_DESCRIPTION_MAX_LENGTH))
    taskComplete = Column(Boolean)
    createdTime = Column(DateTime, default=datetime.utcnow())
    plannedDate = Column(Date, nullable=False)
    completedTime = Column(DateTime, default=None)

    def __init__(self, taskName: str, 
                        plannedDate: datetime.date,
                        taskDescription: str = None):
        self.taskName = taskName
        self.taskDescription = taskDescription
        self.taskComplete = False
        self.plannedDate = datetime.date

    def __repr__(self):
        return "<Task taskId={self.taskId} taskName={self.taskName} complete={self.complete} />"
