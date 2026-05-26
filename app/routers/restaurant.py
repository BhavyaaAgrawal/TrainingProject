from fastapi import APIRouter, Depends
from app.services.restaurant import RestaurantService
from app.dto.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantGetResponse,
    RestaurantListResponse,
)
from app.dependencies import restaurant_service

router = APIRouter(prefix="/restaurant", tags=["Restaurants"])

@router.get("/get-restaurant", response_model=RestaurantGetResponse)
async def get_restaurant(rest_id:int, svc:RestaurantService=Depends(restaurant_service)):
    return await svc.get_restaurant_by_id(rest_id)

@router.get('/get-all-restaurants', response_model=RestaurantListResponse)
async def get_all_restaurants(svc:RestaurantService=Depends(restaurant_service)):
    return await svc.get_all_restaurant()

@router.post("/add-restaurant")
async def add_restaurant(restaurant: RestaurantCreate, svc:RestaurantService=Depends(restaurant_service)):
    restaurant_payload = restaurant.model_dump(exclude_unset=True)
    return await svc.create_new_restaurant(restaurant_payload)

@router.patch("/update-restaurant")
async def update_restaurant(restaurant_id:int, restaurant: RestaurantUpdate,svc:RestaurantService=Depends(restaurant_service)):
    restaurant_payload = restaurant.model_dump(exclude_unset=True, exclude_none=True)
    return await svc.updated_restaurant(restaurant_id, restaurant_payload)

@router.delete("/delete-restaurant")
async def delete_restaurant(restaurant_id:int, svc:RestaurantService=Depends(restaurant_service)):
    return await svc.deleted_restaurant(restaurant_id)

