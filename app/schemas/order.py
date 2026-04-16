from decimal import Decimal
from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    total_amount: Decimal
    final_amount: Decimal


class OrderResponse(BaseModel):
    order_id: int
    total_amount: Decimal
    final_amount: Decimal

    class Config:
        from_attributes = True