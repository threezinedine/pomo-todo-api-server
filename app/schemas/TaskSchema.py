from pydantic import BaseModel


class TaskRequestModel(BaseModel):
    taskName: str
    taskDescription: str
    plannedDate: str

    class Config:
        orm_mode = True


class TaskResponseModel(TaskRequestModel):
    taskId: int
    taskComplete: bool
