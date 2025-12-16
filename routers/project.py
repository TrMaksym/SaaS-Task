from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import schemas, crud
from database import get_db
from dependencies.permissions import require_team_member


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/")
def create_project(
    project: schemas.ProjectCreate,
    member=Depends(require_team_member()),
    db: Session = Depends(get_db),
):
    return crud.create_project(db, project)
