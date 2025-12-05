from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="carts") 
    items: List["CartItem"] = Relationship(back_populates="cart")  

class CartItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(foreign_key="cart.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(default=1)
    cart: Optional[Cart] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="cart_items")
