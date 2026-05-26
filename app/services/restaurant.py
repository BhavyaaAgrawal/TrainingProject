from fastapi import HTTPException, Depends
from app.dto.restaurant import RestaurantCreate, RestaurantUpdate
from app.db.uow import UnitOfWork, get_uow

class RestaurantService():
    def __init__(self, uow):
        self.uow = uow

    async def get_restaurant_by_id(self, rest_id:int):
        restaurant = await self.uow.restaurants.get_restaurant_by_id(rest_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return {"message": "restaurant fetched", "data": restaurant}
    
    async def create_new_restaurant(self, restaurant_payload: RestaurantCreate):
        new_restaurant = await self.uow.restaurants.create_new_restaurant(restaurant_payload)
        return {"message":"Restaurant created", "data": new_restaurant}
    
    
    async def updated_restaurant(self, restaurant_id:int, restaurant_payload: RestaurantUpdate):
        restaurant_exists = await self.uow.restaurants.get_restaurant_by_id(restaurant_id)
        if not restaurant_exists:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        _restaurant = await self.uow.restaurants.update_restaurant(restaurant_exists, restaurant_payload)
        return {"message":"Restaurant updated", "data": _restaurant}
    
    async def deleted_restaurant(self, restaurant_id:int):
        restaurant_exists = await self.uow.restaurants.get_restaurant_by_id(restaurant_id)
        if not restaurant_exists:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        await self.uow.restaurants.delete_restaurant(restaurant_exists)
        return {"message": "Restaurant deleted", "data":[]}
    
    async def get_all_restaurant(self):
        restaurants = await self.uow.restaurants.get_all_restaurants()
        return {"message": "restaurants fetched", "data": restaurants}
