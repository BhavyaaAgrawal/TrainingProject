from typing import List
from fastapi import APIRouter, Depends
from app.dto.cart import CartCreate, CartResponse

from app.services.cart import CartService
from app.dependencies import cart_service

router = APIRouter(
    prefix='/cart', tags=['Cart']
)

@router.post('/add-user-cart')
async def add_user_cart(cart: CartCreate, svc:CartService=Depends(cart_service)):
    cart_payload = cart.model_dump(exclude_unset=True)
    await svc.create_user_cart(cart_payload)
    return {"message": "cart created"}

@router.get('/get-user-cart', response_model=CartResponse)
async def get_user_cart(user_id:int,svc:CartService=Depends(cart_service)):
    user_cart = await svc.get_user_cart(user_id)
    return user_cart

@router.delete('/delete-user-specific-cart')
async def delete_user_cart(user_id:int,cart_id:int, svc:CartService=Depends(cart_service)):
    return await svc.delete_user_cart(user_id, cart_id)

@router.delete('/delete-all-carts-for-user')
async def delete_all_carts_for_user(user_id:int, svc:CartService=Depends(cart_service)):
    return await svc.delete_all_carts_for_user(user_id)
