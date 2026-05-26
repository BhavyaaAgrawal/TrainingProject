from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import Cart
from app.dto.cart import CartCreate


class CartRepository:

    def __init__(self, session:AsyncSession):
        self.session = session

    async def create_user_cart(self, cart_payload:CartCreate):
        user_cart = Cart(**cart_payload)
        self.session.add(user_cart)
        await self.session.flush()
        await self.session.refresh(user_cart)
        return user_cart

    async def get_cart_by_user_id(self, user_id):
        cart = await self.session.execute(select(Cart).where(Cart.user_id == user_id))
        user_cart = cart.scalars().all()
        return user_cart

    async def get_specific_user_cart(self, user_id, cart_id):
        user_cart = await self.session.execute(select(Cart).where(Cart.user_id == user_id).where(Cart.cart_id == cart_id))
        user_cart_model = user_cart.scalar_one_or_none()
        return user_cart_model

    async def get_user_carts(self, user_id):
        user_cart = await self.session.execute(select(Cart).where(Cart.user_id == user_id))
        user_cart_model = user_cart.scalars().all()
        return user_cart_model

    async def delete_user_cart(self, user_cart):
        await self.session.delete(user_cart)
        await self.session.flush()
        return
