from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from app.schemas.common_enums import OrderStatus

class OrderBase(BaseModel):
    user_id: int
    restaurant_id: int
    offer_id: Optional[int]
    total_amount: Decimal
    discount_amount: Optional[Decimal]
    final_amount: Decimal
    order_status: Optional[OrderStatus] = OrderStatus.pending


class OrderCreate(OrderBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class OrderUpdate(BaseModel):
    order_status: Optional[OrderStatus]
    updated_by: Optional[int]


class OrderResponse(OrderBase):
    order_id: int

    class Config:
        from_attributes = True