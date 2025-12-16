from http.client import HTTPException

from fastapi import Depends
from requests import Session
from sqlalchemy.sql import crud

import schemas
from database import get_db
from dependencie.permissions import require_team_member
from routers.auth import router


@router.post("/projects")
def create_project(
    project: schemas.ProjectCreate,
    member=Depends(require_team_member()),
    db: Session = Depends(get_db),
):
    return crud.create_project(db, project)