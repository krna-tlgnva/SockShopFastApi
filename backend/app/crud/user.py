from sqlmodel import Session, select
from app.models.user import User

def createUser(db: Session, username: str, telegram_id: int | None = None, role: str = "user") -> User:
    user = User(username=username, 
                telegram_id=telegram_id, 
                role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def getUser(db: Session, telegram_id: int):
    q = select(User).where(User.telegram_id == telegram_id)
    return db.exec(q).first()

def getFirst(db: Session):
    q = select(User)
    return db.exec(q).first()
