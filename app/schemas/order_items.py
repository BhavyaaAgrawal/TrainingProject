from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class OrderItemBase(BaseModel):
    order_id: int
    item_id: int
    quantity: int
    price: Decimal


class OrderItemCreate(OrderItemBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class OrderItemResponse(OrderItemBase):
    order_item_id: int

    class Config:
        from_attributes = True