from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

import crud, schemas
from database import get_db

router = APIRouter(
    prefix="/users",
)

@router.post("/", response_model=schemas.TaskRead)
def create_task(task: schemas.TaskCreate,user_id: int, db: Session = Depends(get_db)):
    return crud.create_task(task=task, db=db, user_id=current_user.id)