from fastapi import APIRouter, Depends
from app.dto.order import OrderCreate, OrderGetResponse, OrderListResponse
from app.services.orders import OrderService
from app.dependencies import order_service

router = APIRouter(
    prefix="/orders", tags=["Orders"]
)

@router.post('/add-order')
async def add_order(order:OrderCreate, svc:OrderService=Depends(order_service)):
    order_payload = order.model_dump(exclude_unset=True)
    return await svc.create_order(order_payload)

@router.get('/get-order', response_model=OrderGetResponse)
async def get_user_order(order_id:int, svc:OrderService=Depends(order_service)):
    return await svc.get_order(order_id)

@router.get('/get-user-order', response_model=OrderListResponse)
async def get_user_orders(user_id:int, svc:OrderService=Depends(order_service)):
    return await svc.get_user_orders(user_id)
