from pydantic import (
    BaseModel,
)
from datetime import date


class TaskRequestModel(BaseModel):
    taskName: str
    taskDescription: str
    plannedDate: date

    class Config:
        orm_mode = True


class TaskResponseModel(TaskRequestModel):
    taskId: int
    userId: int
    taskComplete: bool
