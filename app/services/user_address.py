from fastapi import HTTPException

from app.db.uow import UnitOfWork

class UserAddressService:
    def __init__(self, uow:UnitOfWork):
        # this uow is set from app/db/uow file itself while initiating repositories there
        print('uow============', uow)
        print('current uow session========', uow.session)
        self.uow = uow

    async def add_address(self, address_payload):
        """ This method will add a new address to system """
        # check if address is not associated any other user
        address_exists = await self.uow.addresses.get_address(address_payload['address_line'])
        if address_exists:
            raise HTTPException(status_code=400, detail="Address already exists")
        await self.uow.addresses.add_address(address_payload)
        return {"message": "Address added successfully", "data":[]}

    async def get_address_for_user(self, user_id):
        user_address = await self.uow.addresses.get_user_address(user_id)
        if not user_address:
            raise HTTPException(status_code=404, detail=f"No address found for user :{user_id}")
        return {"message": "Address added successfully", "data":[user_address]}

    async def updated_user_address(self, user_id, address_payload):
        await  self.uow.addresses.update_user_address(user_id, address_payload)
        return {"message": "Address updated successfully", "data": []}

    async def delete_user_address(self, user_id):
        user = await self.uow.addresses.get_user_address(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"No address found for user :{user_id}")
        await self.uow.addresses.delete_user_address(user)
        return {"message": "Address deleted successfully", "data": []}