from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

from app.dto.common_enums import RestaurantStatus


class RestaurantBase(BaseModel):
    name: str
    address: Optional[str]
    phone_number: Optional[str]
    status: Optional[RestaurantStatus] = RestaurantStatus.active
    image: Optional[str]


class RestaurantCreate(RestaurantBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[RestaurantStatus] = None
    updated_by: Optional[int] = None
    image: Optional[str] = None


class RestaurantResponse(RestaurantBase):
    restaurant_id: int

    class Config:
        from_attributes = True


class RestaurantGetResponse(BaseModel):
    message: str
    data: RestaurantResponse


class RestaurantListResponse(BaseModel):
    message: str
    data: List[RestaurantResponse]
