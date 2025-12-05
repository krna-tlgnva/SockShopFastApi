from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    telegram_id: Optional[int] = Field(default=None, index=True)
    role: str = Field(default="user")
    carts: List["Cart"] = Relationship(back_populates="user")
    purchases: List["Purchase"] = Relationship(back_populates="user")
