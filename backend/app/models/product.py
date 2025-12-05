from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: int
    description: Optional[str] = None
    cart_items: List["CartItem"] = Relationship(back_populates="product")
    purchases: List["Purchase"] = Relationship(back_populates="product")
