from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    telegram_id: Optional[int] = None
    role: Optional[str] = "user"

class UserOut(UserCreate):
    id: int
