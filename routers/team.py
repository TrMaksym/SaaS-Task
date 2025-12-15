from fastapi import Depends
from requests import Session

import crud
import schemas
from database import get_db
from dependencies import get_current_user
from models import User
from routers.auth import router
from schemas import TeamCreate


@router.post("/team")
def create_team(
    team: schemas.TeamCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_team(db, team, user.id)