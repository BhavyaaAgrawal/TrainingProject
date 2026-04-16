from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class MenuItemBase(BaseModel):
    restaurant_id: int
    name: str
    description: Optional[str]
    price: Decimal
    is_veg: Optional[bool]
    is_available: Optional[bool]


class MenuItemCreate(MenuItemBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class MenuItemUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    is_veg: Optional[bool]
    is_available: Optional[bool]
    updated_by: Optional[int]


class MenuItemResponse(MenuItemBase):
    item_id: int

    class Config:
        from_attributes = True