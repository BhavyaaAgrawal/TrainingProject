from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import UserAddress
from app.dto.user_address import AddressCreate, AddressUpdate


class AddressRepository:

    def __init__(self, session:AsyncSession):
        self.session = session

    async def add_address(self, address_payload:AddressCreate):
        address = UserAddress(**address_payload)
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address

    async def get_address(self, address_line):
        address = await self.session.execute(select(UserAddress).where(UserAddress.address_line == address_line))
        address = address.scalar_one_or_none()
        return address

    async def get_user_address(self, user_id):
        address = await self.session.execute(select(UserAddress).where(UserAddress.user_id == user_id))
        user_address = address.scalar_one_or_none()
        return user_address

    async def update_user_address(self, user_id, address_payload:AddressUpdate):
        user_address = await self.get_user_address(user_id)
        for key, value in address_payload.items():
            setattr(user_address, key, value)
        self.session.add(user_address)
        await self.session.commit()
        await self.session.refresh(user_address)
        return user_address

    async def delete_user_address(self, user):
        await self.session.delete(user)
        await self.session.flush()