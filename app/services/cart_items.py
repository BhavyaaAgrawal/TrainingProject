from app.dto.cart_items import CartItemCreate
from app.db.uow import UnitOfWork

class CartItemService:
    def __init__(self, uow:UnitOfWork):
        self.uow = uow

    async def add_cart_item(self, cart_item:CartItemCreate):
        cart_item = await self.uow.cart_items.add_cart_item(cart_item)
        return {"message": "Item added in cart successfully", "data": cart_item}
