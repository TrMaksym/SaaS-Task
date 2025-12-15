from http.client import HTTPException

from fastapi import Depends
from requests import Session
from sqlalchemy.sql import crud

import schemas
from database import get_db
from dependencies import get_current_user
from models import User
from routers.auth import router


@router.post("/project")
def create_project(
    project: schemas.ProjectCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = crud.create_project(db, project, user.id)
    if not project:
        raise HTTPException(403, "Access denied")
    return project