from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
import models
from database import get_db
from dependencies.auths import require_admin

router = APIRouter(
    prefix="/users",
)

@router.post("/create", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), admin = Depends(require_admin)):
    try:
        hashed_password = crud.pwd_context.hash(user.password)
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user