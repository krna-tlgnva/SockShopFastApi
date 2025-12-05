from pydantic import BaseModel
from typing import Optional

class AddToCartIn(BaseModel):
    product_id: int
    quantity: int = 1
    telegram_id: Optional[int] = None
