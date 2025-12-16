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

@router.post("/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate,
                current_user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task, user_id=current_user.id)

@router.get("/", response_model=List[schemas.TaskRead])
def read_tasks(status: Optional[models.TaskStatus] = None,
               current_user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id)
    if status:
        tasks = tasks.filter(models.Task.status == status)
    return tasks.all()

@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int,
                task_update: schemas.TaskUpdate,
                current_user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    task = crud.update_task(db=db, task_id=task_id, task_update=task_update, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", response_model=schemas.TaskRead)
def delete_task(
    task_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = crud.delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
