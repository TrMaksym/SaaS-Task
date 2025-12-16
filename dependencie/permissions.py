
from fastapi import Depends, HTTPException
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models, crud
from database import get_db
from dependencies import get_current_user


def require_team_member(allow_owner_only: bool = False):
    def dependency(
        team_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
    ):
        member = crud.get_team_member(db, team_id, current_user.id)
        if not member:
            raise HTTPException(status_code=403, detail="Access denied")

        if allow_owner_only and member.role != models.TeamRole.OWNER:
            raise HTTPException(status_code=403, detail="Owner only")

        return member

    return dependency