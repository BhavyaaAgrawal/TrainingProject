from pydantic import BaseModel, EmailStr
from typing import Optional

class AddressBase(BaseModel):
    user_id: int
    address_line: str
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    is_default: Optional[bool] = False


class AddressCreate(AddressBase):
    created_by: Optional[int]
    updated_by: Optional[int]


class AddressUpdate(BaseModel):
    address_line: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]
    is_default: Optional[bool]
    updated_by: Optional[int]


class AddressResponse(AddressBase):
    address_id: int

    class Config:
        from_attributes = True