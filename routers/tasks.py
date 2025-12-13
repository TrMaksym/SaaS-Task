from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

import crud, schemas
import models
from database import get_db
from dependencies import get_current_user

router = APIRouter(
    prefix="/users",
)

@router.post("/", response_model=schemas.TaskRead)
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_task(
        db=db,
        task=task,
        user_id=current_user.id
    )