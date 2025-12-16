from http.client import HTTPException

from fastapi import Depends, APIRouter
from requests import Session
from sqlalchemy.sql import crud

import schemas
from database import get_db
from dependencies import get_current_user
from models import User


router = APIRouter()

def require_team_member_from_body():
    def dependency(
        project: schemas.ProjectCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        member = crud.get_team_member(db, project.team_id, user.id)
        if not member:
            raise HTTPException(403)
        return member
    return dependency
