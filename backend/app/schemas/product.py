from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: int
    description: Optional[str] = None

class ProductOut(ProductCreate):
    id: int
