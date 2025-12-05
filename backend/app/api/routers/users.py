from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud import user as crud_user

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, payload.username, payload.telegram_id, payload.role)
