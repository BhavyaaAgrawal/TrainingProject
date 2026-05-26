from typing import Optional, List
from pydantic import BaseModel, RootModel, ConfigDict
from datetime import datetime


class CartBase(BaseModel):
    user_id: int
    restaurant_id: int



class CartCreate(CartBase):
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class CartResponse(BaseModel):
    message: str
    data: List[CartOut]


class CartOut(CartBase):
    model_config = ConfigDict(from_attributes=True)

    cart_id: int
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
