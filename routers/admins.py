from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


import schemas, crud
from database import get_db
from dependencies.auths import require_admin
from models import User

router = APIRouter(
    prefix="/admins",
    tags=["admin-management"],
)

@router.post("/create/admin", response_model=schemas.UserRead)
def create_user_admin(
        user: schemas.UserCreate,
        current_user: User = Depends(require_admin),
        db: Session = Depends(get_db)
):
    return crud.create_user(db, user)

def create_admin(db: Session, user: schemas.UserCreate):
    hashed_password = crud.pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        is_admin=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
