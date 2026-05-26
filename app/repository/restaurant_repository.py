from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import Restaurant
from app.dto.restaurant import RestaurantCreate, RestaurantUpdate


class RestaurantRepository:

    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_restaurant_by_id(self, restaurant_id: int):
        restaurant = await self.session.execute(select(Restaurant).where(Restaurant.restaurant_id == restaurant_id))
        restaurant_model = restaurant.scalar_one_or_none()
        return restaurant_model

    async def create_new_restaurant(self, restaurant_payload: RestaurantCreate):
        restaurant = Restaurant(**restaurant_payload)
        self.session.add(restaurant)
        await self.session.flush()
        await self.session.refresh(restaurant)
        return restaurant

    async def update_restaurant(self, restaurant, restaurant_payload: RestaurantUpdate):
        for key, value in restaurant_payload.items():
            setattr(restaurant, key, value)
        await self.session.flush()
        await self.session.refresh(restaurant)
        return restaurant

    async def delete_restaurant(self, restaurant):
        await self.session.delete(restaurant)
        await self.session.flush()
        return {"message": "restaurant deleted"}

    async def get_all_restaurants(self):
        restaurants = await self.session.execute(select(Restaurant))
        restaurant_model = restaurants.scalars().all()
        return restaurant_model
