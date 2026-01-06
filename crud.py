import hashlib
import secrets
import token
import uuid
from datetime import datetime, timedelta

from minio.time import utcnow
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

import models, schemas
from passlib.context import CryptContext

from core.security import _prehash_password, get_password_hash
from dependencies.permissions import get_team_member

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = (models.Task(
        title=task.title,
        description=task.description,
        owner_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=utcnow(),
    ))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user_id
    ).first()
    if not task:
        return None
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    task.updated_at = utcnow()
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return task


def create_team(db: Session, team: schemas.TeamCreate, owner_id: int):
    db_team = models.Team(name=team.name, owner_id=owner_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    owner_member = models.TeamMember(user_id=owner_id, team_id=team.id, role=models.TeamRole.OWNER)
    db.add(owner_member)
    db.commit()
    return db_team

def update_team(
    db: Session,
    team_id: int,
    team_update: schemas.TeamUpdate,
    current_user_id: int
):
    member = get_team_member(db, team_id, current_user_id)
    if not member or member.role != models.TeamRole.OWNER:
        return None

    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if not team:
        return None

    if team_update.name is not None:
        team.name = team_update.name

    team.updated_at = utcnow()
    db.commit()
    db.refresh(team)
    return team


def project_create(db: Session, project: schemas.ProjectCreate, team_id: int):
    member = get_team_member(db, project.team_id, current_user.id)
    if not member:
        return None

    db_project = models.Project(
        name=project.name,
        team_id=project.team_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def accept_invite(db: Session, invite_id: int, current_user_id: int):
    invite = db.query(models.TeamInvite).filter(
        models.TeamInvite.token == token,
        models.TeamInvite.expires_at > datetime.utcnow()
    ).first()

    if not invite:
        return None

    member = models.TeamMember(
        user_id=current_user_id,
        team_id=invite.team_id,
        role=models.TeamRole.MEMBER
    )
    db.add(member)

    db.delete(invite)
    db.commit()
    return (
        member
    )

def log_activity(db: Session, team_id: int, user_id: int, action: str, entity_type: str, entity_id: int):
    activity = models.Activity(team_id=team_id, user_id=user_id, action=action, entity_type=entity_type, entity_id=entity_id)
    db.add(activity)
    db.commit()

def create_team_invite(db: Session, invited_by: int, team_id: int, email: str, role: models.TeamRole):
    token_str = secrets.token_urlsafe(16)
    invite = models.TeamInvite(
        email=email,
        team_id=team_id,
        role=role,
        token=token_str,
        invited_by=invited_by,
        expires_at=datetime.utcnow() + timedelta(days=3)
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite

def assign_user_to_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).get(task_id)
    user = db.query(models.User).get(user_id)
    if not task or not user:
        return None
    task.assignees.append(user)
    db.commit()
    db.refresh(task)
    return task

def add_comment(db: Session, task_id, user_id, content: str):
    comment = models.TaskComment(task_id=task_id, user_id=user_id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_task_comments(db: Session, task_id: int):
    return db.query(models.TaskComment).filter(models.TaskComment.task_id == task_id).all()