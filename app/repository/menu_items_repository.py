from sqlalchemy import select

from app.orm import MenuItem
from app.dto.menu_item import MenuItemCreate, MenuItemUpdate


class ItemRepository:

    def __init__(self, session):
        self.session = session

    async def get_item_by_id(self,item_id: int):
        item = await self.session.execute(select(MenuItem).where(MenuItem.item_id==item_id))
        item_model = item.scalar_one_or_none()
        return item_model

    async def add_item_to_db(self, item_payload:MenuItemCreate):
        item_to_add = MenuItem(**item_payload)
        self.session.add(item_to_add)
        await self.session.flush()
        await self.session.refresh(item_to_add)
        return item_to_add

    async def update_existing_item(self, item, item_payload:MenuItemUpdate):
        for key, value in item_payload.items():
            setattr(item, key, value)
        await self.session.flush()
        await self.session.refresh(item)
        return item

    async def get_all_menu_items(self):
        items = await self.session.execute(select(MenuItem))
        items_model = items.scalars().all()
        return items_model

    async def delete_item(self, item_id:int):
        item = await self.session.execute(select(MenuItem).where(MenuItem.item_id==item_id))
        await self.session.delete(item)
        await self.session.flush()
        return {"message": "Item deleted"}

    async def fetch_restaurant_items(self, restaurant_id:int):
        rest_items = await self.session.execute(select(MenuItem).where(MenuItem.restaurant_id==restaurant_id))
        items = rest_items.scalars().all()
        return items