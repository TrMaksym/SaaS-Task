from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
from core.security import verify_password, create_access_token
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="incorrect email or password")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="incorrect email or password")

    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
