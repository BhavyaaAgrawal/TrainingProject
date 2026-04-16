from pydantic import BaseModel
from typing import Optional
from enum import Enum

from app.schemas.common_enums import RestaurantStatus


class RestaurantBase(BaseModel):
    name: str
    address: Optional[str]
    phone_number: Optional[str]
    status: Optional[RestaurantStatus] = RestaurantStatus.active


class RestaurantCreate(RestaurantBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class RestaurantUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]
    status: Optional[RestaurantStatus]
    updated_by: Optional[int]


class RestaurantResponse(RestaurantBase):
    restaurant_id: int

    class Config:
        from_attributes = True