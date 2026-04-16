from pydantic import BaseModel
from typing import Optional

class CartBase(BaseModel):
    user_id: int
    restaurant_id: int


class CartCreate(CartBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class CartResponse(CartBase):
    cart_id: int

    class Config:
        from_attributes = True