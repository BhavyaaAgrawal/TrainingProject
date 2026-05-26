from fastapi import HTTPException
from app.dto.cart import CartCreate
from app.db.uow import UnitOfWork


class CartService:

    def __init__(self, uow:UnitOfWork):
        self.uow = uow

    # @staticmethod
    async def create_user_cart(self, cart_payload:CartCreate):
        user_cart = await self.uow.carts.create_user_cart(cart_payload)
        return {"message": "User cart created successfully", "data": user_cart}

    async def get_user_cart(self, user_id):
        user_cart = await self.uow.carts.get_cart_by_user_id(user_id)
        if not user_cart:
            raise HTTPException(status_code=404, detail=f"No cart found for user:{user_id}")
        return {"message": "User fetched successfully", "data": user_cart}

    async def delete_user_cart(self, user_id, cart_id):
        user_cart = await self.uow.carts.get_specific_user_cart(user_id, cart_id)
        if not user_cart:
            raise HTTPException(status_code=404, detail=f"No cart found for user:{user_id}")
        await self.uow.carts.delete_user_cart(user_cart)
        return {"message": f"cart with id: {cart_id} deleted successfully", "data":[]}

    async def delete_all_carts_for_user(self, user_id):
        user_carts = await self.uow.carts.get_user_carts(user_id)
        if not user_carts:
            raise HTTPException(status_code=404, detail=f"No cart found for user:{user_id}")
        for cart in user_carts:
            await self.uow.carts.delete_user_cart(cart)
        return {"message": f"all carts for user with id:{user_id} deleted successfully"}