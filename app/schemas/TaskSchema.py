import datetime
from typing import (
    Union,
)
from pydantic import (
    BaseModel,
)
from datetime import date, datetime


class TaskRequestModel(BaseModel):
    taskName: str
    taskDescription: str
    plannedDate: date

    class Config:
        orm_mode = True


class TaskCompleteRequestModel(BaseModel):
    taskId: int
    completedTime: datetime

    class Config:
        orm_mode = True


class TaskResponseModel(TaskRequestModel):
    taskId: int
    userId: int
    taskComplete: bool
    completedTime: Union[datetime, None]
