import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base


class TaskStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TeamRole(str, enum.Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class TeamInvite(Base):
    __tablename__ = "team_invites"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    role = Column(Enum(TeamRole), default=TeamRole.MEMBER)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)

    team = relationship("Team")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    members = relationship("TeamMember", back_populates="team.py")
    project = relationship("Project", back_populates="team.py")


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


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_done = Column(Boolean, default=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)

    owner = relationship("User", back_populates="tasks")
