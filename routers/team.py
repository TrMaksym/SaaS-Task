from fastapi import Depends, APIRouter, HTTPException
from requests import Session

import crud
import schemas
from database import get_db
from dependencies.auths import get_current_user
from models import User, TeamInvite

router = APIRouter(
    prefix="/team",
    tags=["team"],
)

@router.post("/")
def create_team(
    team: schemas.TeamCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_team(db, team, user.id)

@router.put("/{team_id}")
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


@router.post("/{team_id}/invite", response_model=schemas.TeamInviteRead)
def invite_user(
    team_id: int,
    invite: schemas.TeamInviteCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_team_invite(
        db=db,
        team_id=team_id,
        email=invite.email,
        role=invite.role,
        invited_by=user.id,
    )