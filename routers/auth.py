from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db
from core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/create")
def create_user_endpoint(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        return crud.create_user(db, user_data)
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=400, detail=str(e))