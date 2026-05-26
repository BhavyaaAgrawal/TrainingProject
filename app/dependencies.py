#initiate UserAddressService here and pass uow object from here
from fastapi import Depends

from app.db.uow import UnitOfWork, get_uow
from app.services.user_address import UserAddressService
from app.services.user_service import UserService
from app.services.restaurant import RestaurantService
from app.services.orders import OrderService
from app.services.item_service import MenuItemService
from app.services.cart import CartService
from app.services.cart_items import CartItemService
from app.services.background_tasks_service import BackgroundTasksService


def get_user_address_service(
    uow: UnitOfWork = Depends(get_uow),
) -> UserAddressService:
    return UserAddressService(uow=uow)

def user_service(
        uow: UnitOfWork=Depends(get_uow))->UserService:
    return UserService(uow)

def restaurant_service(
        uow:UnitOfWork=Depends(get_uow))->RestaurantService:
    return RestaurantService(uow)

def order_service(uow:UnitOfWork=Depends(get_uow))->OrderService:
    return OrderService(uow)

def menu_item_service(uow:UnitOfWork=Depends(get_uow))->MenuItemService:
    return MenuItemService(uow=uow)

def cart_service(uow:UnitOfWork=Depends(get_uow))->CartService:
    return CartService(uow=uow)

def cart_item_service(uow:UnitOfWork=Depends(get_uow))->CartItemService:
    return CartItemService(uow=uow)

# def background_tasks_service():
#     return BackgroundTasksService()