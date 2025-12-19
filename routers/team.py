import datetime
import secrets
from http.client import HTTPException

from fastapi import Depends, APIRouter
from requests import Session

import crud
import schemas
from database import get_db
from dependencies.auths import get_current_user
from models import User, TeamRole, TeamInvite

router = APIRouter(
    prefix="/team",
    tags=["team"],
)

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

def create_team_invite(db: Session, team_id: int, email: str, role: TeamRole):
    token = secrets.token_urlsafe(16)
    invite = TeamInvite(
        email=email,
        team_id=team_id,
        role=role,
        token=token,
        expires_at=datetime.utcnow() + datetime.timedelta(days=3)
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite

