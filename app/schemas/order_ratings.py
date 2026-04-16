from pydantic import BaseModel
from typing import Optional

class OrderRatingBase(BaseModel):
    order_id: int
    user_id: int
    restaurant_id: int
    rating: int
    review: Optional[str]


class OrderRatingCreate(OrderRatingBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class OrderRatingResponse(OrderRatingBase):
    rating_id: int

    class Config:
        from_attributes = True