from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import crud, schemas, models
from database import get_db
from dependencies.auths import get_current_user
from models import TaskComment

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

def require_task_access(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.Task:
    task = (
        db.query(models.Task)
        .join(models.Project)
        .filter(models.Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    team_member = crud.get_team_member(
        db=db,
        team_id=task.project.team_id,
        user_id=current_user.id
    )

    if not team_member:
        raise HTTPException(status_code=403, detail="Access denied")

    return task

@router.post("/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate,
                current_user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    task = crud.create_task(db=db, task=task, user_id=current_user.id)

    crud.log_activity(
        db=db,
        user_id=current_user.id,
        team_id=task.project.team_id,
        action="created",
        entity_type="task",
        entity_id=task.id
    )
    return task
def read_tasks(
    project_id: Optional[int] = None,
    status: Optional[models.TaskStatus] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task).join(models.Project).join(models.TeamMember)\
        .filter(models.TeamMember.user_id == current_user.id)
    if project_id:
        query = query.filter(models.Project.id == project_id)
    if status:
        query = query.filter(models.Task.status == status)
    if search:
        query = query.filter(models.Task.title.ilike(f"%{search}%"))
    if sort_by in ["created_at", "updated_at", "status"]:
        query = query.order_by(getattr(models.Task, sort_by).desc())
    return query.all()

@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_in: schemas.TaskUpdate,
    task: models.Task = Depends(require_task_access),
    db: Session = Depends(get_db),
):
    updated_task = crud.update_task(
        db=db,
        task_id=task.id,
        task_update=task_in,
        user_id=task.owner_id,
    )

    crud.log_activity(
        db=db,
        user_id=task.owner_id,
        team_id=task.project.team_id,
        action="updated",
        entity_type="task",
        entity_id=task.id
    )
    return updated_task


@router.delete("/{task_id}", response_model=schemas.TaskRead)
def delete_task(
    task: models.Task = Depends(require_task_access),
    db: Session = Depends(get_db),
):
    deleted_task = crud.delete_task(db=db, task_id=task.id, user_id=task.owner_id)

    crud.log_activity(
        db=db,
        user_id=task.owner_id,
        team_id=task.project.team_id,
        action="deleted",
        entity_type="task",
        entity_id=task.id
    )
    return deleted_task

def assign_user_to_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).get(task_id)
    user = db.query(models.User).get(user_id)
    if not task or not user:
        return False
    task.assignees.append(user)
    db.commit()
    db.refresh(task)
    return task

def add_comment(db: Session, task_id, user_id, content: str):
    comment = TaskComment(task_id=task_id, user_id=user_id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def get_task_comments(db: Session, task_id: int):
    return db.query(TaskComment).filter(TaskComment.task_id == task_id).all()