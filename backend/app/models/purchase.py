from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Purchase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(default=1)
    date: datetime = Field(default_factory=datetime.utcnow)
    user: Optional["User"] = Relationship(back_populates="purchases")
    product: Optional["Product"] = Relationship(back_populates="purchases")
