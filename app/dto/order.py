from pydantic import BaseModel, RootModel, ConfigDict
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.dto.common_enums import OrderStatus

class OrderBase(BaseModel):
    user_id: int
    restaurant_id: int
    offer_id: Optional[int] = None
    total_amount: Decimal
    discount_amount: Optional[Decimal] = None
    final_amount: Decimal
    order_status: Optional[OrderStatus] = OrderStatus.pending


class OrderCreate(OrderBase):
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class OrderUpdate(BaseModel):
    order_status: Optional[OrderStatus] = None
    updated_by: Optional[int] = None


class OrderGetResponse(BaseModel):
    message: str
    data: "OrderOut"


class OrderListResponse(BaseModel):
    message: str
    data: List["OrderOut"]


# Output schema for ORM Order objects.
class OrderOut(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class OrderResponse(OrderOut):
    # Backwards-compatible alias for older imports.
    pass
