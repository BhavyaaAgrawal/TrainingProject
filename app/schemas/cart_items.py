from pydantic import BaseModel
from typing import Optional

class CartItemBase(BaseModel):
    cart_id: int
    item_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class CartItemUpdate(BaseModel):
    quantity: Optional[int]
    updated_by: Optional[int]


class CartItemResponse(CartItemBase):
    cart_item_id: int

    class Config:
        from_attributes = True