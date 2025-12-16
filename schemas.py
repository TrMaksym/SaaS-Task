from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models import TaskStatus, TeamRole



class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class TeamMemberRead(BaseModel):
    user_id: int
    team_id: int
    role: TeamRole

    class Config:
        from_attributes = True


class TeamUpdate(BaseModel):
    name: Optional[str] = None


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    team_id: int


class ProjectRead(ProjectBase):
    id: int
    team_id: int

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    project_id: int
    assignee_id: int
    status: TaskStatus = TaskStatus.TODO


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_id: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    assignee_id: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
