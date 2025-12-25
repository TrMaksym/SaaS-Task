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


class TeamUpdate(BaseModel):
    name: Optional[str] = None


class TeamMemberRead(BaseModel):
    user_id: int
    team_id: int
    role: TeamRole

    class Config:
        from_attributes = True


class TeamRead(TeamBase):
    id: int
    owner_id: int
    members: List[TeamMemberRead] = []

    class Config:
        from_attributes = True


class TeamInviteCreate(BaseModel):
    email: str
    role: TeamRole


class TeamInviteRead(BaseModel):
    id: int
    email: str
    team_id: int
    role: TeamRole
    token: str
    expires_at: datetime

    class Config:
        from_attributes = True


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
    assignee_ids: List[int] = []
    status: TaskStatus = TaskStatus.TODO


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assignee_ids: Optional[List[int]] = None


class TaskRead(TaskBase):
    id: int
    project_id: int
    status: TaskStatus
    assignees: List[UserRead] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str


class CommentRead(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ActivityRead(BaseModel):
    id: int
    user_id: int
    team_id: int
    action: str
    entity_type: str
    entity_id: int
    created_at: datetime

    class Config:
        from_attributes = True
