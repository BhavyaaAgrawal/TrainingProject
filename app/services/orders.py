from fastapi import HTTPException
from app.dto.order import OrderCreate
from app.core.exceptions import error_codes, error_messages
from app.core.exceptions.domain import NotFoundError
from app.db.uow import UnitOfWork

class OrderService:
    def __init__(self, uow:UnitOfWork):
        self.uow = uow

    async def get_order(self, order_id):
        order = await self.uow.orders.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"message": "Order fetched", "data": order}
    
    
    async def create_order(self, order_payload:OrderCreate):
        user = await self.uow.users.get_user_by_id(order_payload['user_id'])
        if user is None:
            raise NotFoundError(error_codes.USER_NOT_FOUND,
                                error_messages.USER_NOT_FOUND)
        order = await self.uow.orders.create_order(order_payload)
        return {"message": "Order created successfully", "data": order}
    
    async def get_user_orders(self, user_id:int):
        orders = await self.uow.orders.get_user_orders(user_id)
        if not orders:
            raise HTTPException(status_code=404, detail=f"No order found for user: {user_id}")
        return {"message": "Orders fetched", "data": orders}
