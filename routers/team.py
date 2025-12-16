from http.client import HTTPException

from fastapi import Depends, APIRouter
from requests import Session

import crud
import schemas
from database import get_db
from dependencies import get_current_user
from models import User
from routers.auth import router
from schemas import TeamCreate

router = APIRouter()

@router.post("/team")
def create_team(
    team: schemas.TeamCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_team(db, team, user.id)

@router.put("/team/{team_id}")
def update_team(
    team_id: int,
    team: schemas.TeamUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = crud.update_team(db, team_id, team, user.id)
    if not updated:
        raise HTTPException(status_code=403, detail="Access denied")
    return updated

