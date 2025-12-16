from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import crud, schemas, models
from database import get_db
from dependencies.auths import get_current_user

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

def require_task_access(task_id_param: str = "task_id"):
    def dependency(
            task_id: int = Depends(),
            db: Session = Depends(get_db),
            current_user: models.User = Depends(get_current_user),
    ):
        task = db.query(models.Task).filter(models.Task.id == task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        project = task.project
        team_member = crud.get_team_member(db, project.team_id, current_user.id)
        if not team_member:
            raise HTTPException(status_code=403, detail="Access denied")
        return task
    return dependency

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
@router.get("/", response_model=List[schemas.TaskRead])
def read_tasks(
    project_id: Optional[int] = None,
    status: Optional[models.TaskStatus] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Task).join(models.Project).join(models.TeamMember)\
        .filter(models.TeamMember.user_id == current_user.id)
    if project_id:
        query = query.filter(models.Project.id == project_id)
    if status:
        query = query.filter(models.Task.status == status)

    return query.all()

@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    task: models.Task = Depends(require_task_access("task_id")),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_task = crud.update_task(db=db, task_id=task_id, task_update=task_in, user_id=current_user.id)

    crud.log_activity(
        db=db,
        user_id=current_user.id,
        team_id=task.project.team_id,
        action="updated",
        entity_type="task",
        entity_id=task.id
    )
    return update_task

@router.delete("/{task_id}", response_model=schemas.TaskRead)
def delete_task(
    task_id: int,
    task: models.Task = Depends(require_task_access("task_id")),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deleted_task = crud.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    crud.log_activity(
        db=db,
        user_id=current_user.id,
        team_id=task.project.team_id,
        action="deleted",
        entity_type="task",
        entity_id=task.id
    )
    return deleted_task