from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import TaskStatus

# ----------------- User -----------------
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

# ----------------- Task -----------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    status: Optional[TaskStatus] = TaskStatus.TODO

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus]

class TaskRead(TaskBase):
    id: int
    owner_id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
