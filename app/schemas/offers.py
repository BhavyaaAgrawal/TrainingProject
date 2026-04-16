from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from app.schemas.common_enums import DiscountType


class OfferBase(BaseModel):
    code: str
    description: Optional[str]
    discount_type: Optional[DiscountType]
    discount_value: Optional[Decimal]
    min_order_amount: Optional[Decimal]
    max_discount_amount: Optional[Decimal]
    valid_from: Optional[str]
    valid_to: Optional[str]
    is_active: Optional[bool]


class OfferCreate(OfferBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class OfferUpdate(BaseModel):
    description: Optional[str]
    discount_type: Optional[DiscountType]
    discount_value: Optional[Decimal]
    is_active: Optional[bool]
    updated_by: Optional[int]


class OfferResponse(OfferBase):
    offer_id: int

    class Config:
        from_attributes = True