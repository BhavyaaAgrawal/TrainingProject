from sqlalchemy.ext.asyncio import AsyncSession

from app.dto.cart_items import CartItemCreate
from app.orm import CartItem


class CartItemRepository:
    def __init__(self, session:AsyncSession):
        self.session = session

    async def add_cart_item(self, cart_item:CartItemCreate):
        cart_item = CartItem(**cart_item)
        self.session.add(cart_item)
        await self.session.flush()
        await self.session.refresh(cart_item)
        return cart_item