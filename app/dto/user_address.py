from pydantic import BaseModel, EmailStr
from typing import Optional

class AddressBase(BaseModel):
    user_id: int
    address_line: str
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    is_default: Optional[bool] = False


class AddressCreate(AddressBase):
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class AddressUpdate(BaseModel):
    address_line: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    is_default: Optional[bool] = False
    updated_by: Optional[int] = None


class AddressResponse(AddressBase):
    address_id: int

    class Config:
        from_attributes = True