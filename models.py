import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Table, Text
from sqlalchemy.orm import relationship
from database import Base


task_assignees = Table(
    "task_assignees",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True, nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
)

class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TeamRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class TaskComment(Base):
    __tablename__ = "task_comments"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")

class TeamInvite(Base):
    __tablename__ = "team_invites"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    role = Column(Enum(TeamRole), default=TeamRole.MEMBER)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    invited_by = Column(Integer, ForeignKey("users.id"))

    team = relationship("Team", back_populates="invites")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    entity_type = Column(String)
    entity_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    members = relationship("TeamMember", back_populates="team")
    projects = relationship("Project", back_populates="team")
    invites = relationship("TeamInvite", back_populates="team")

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    role = Column(Enum(TeamRole), default=TeamRole.MEMBER)

    user = relationship("User", back_populates="teams")
    team = relationship("Team", back_populates="members")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="owner")
    assigned_tasks = relationship(
        "Task",
        secondary=task_assignees,
        back_populates="task_assignees"
    )
    comments = relationship("TaskComment", back_populates="user")
    teams = relationship("TeamMember", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_done = Column(Boolean, default=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)

    owner = relationship("User", back_populates="tasks")
    task_assignees = relationship(
        "User",
        secondary=task_assignees,
        back_populates="assigned_tasks"
    )
    comments = relationship("TaskComment", back_populates="task")
    project = relationship("Project", back_populates="tasks")