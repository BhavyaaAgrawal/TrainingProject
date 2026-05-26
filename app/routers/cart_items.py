from fastapi import APIRouter, Depends
from app.dto.cart_items import CartItemCreate
from app.dependencies import cart_item_service
from app.services.cart_items import CartItemService

router = APIRouter(prefix='/cart-items',
                   tags=['CartItems'])

@router.post('/add-cart-item')
async def add_cart_item(cart_payload:CartItemCreate,
                        svc:CartItemService=Depends(cart_item_service)):
    item_payload =  cart_payload.model_dump(exclude_none=True, exclude_unset=True)
    return await svc.add_cart_item(item_payload)