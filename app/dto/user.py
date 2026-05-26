from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str
    created_by: Optional[int] = None
    updated_by: Optional[int] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    updated_by: Optional[int] = None


class UserResponse(UserBase):
    user_id: int
    is_deleted: bool

    #this from_attributes is used to tell pydantic to convert the data as orm else in response we would be getting
    # response like dict but now we can get user.name, user.email etc...
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str