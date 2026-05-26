from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import Order
from app.dto.order import OrderCreate


class OrderRepository:
    
    def __init__(self, session:AsyncSession):
        self.session = session
    
    async def create_order(self, order_payload:OrderCreate):
        order = Order(**order_payload)
        self.session.add(order)
        await self.session.flush()
        await self.session.refresh(order)
        return order

    async def get_order_by_id(self, order_id:int):
        order = await self.session.execute(select(Order).where(Order.order_id == order_id))
        order_model = order.scalar_one_or_none()
        return order_model

    async def get_user_orders(self, user_id:int):
        orders = await self.session.execute(select(Order).where(Order.user_id == user_id))
        user_orders = orders.scalars().all()
        return user_orders