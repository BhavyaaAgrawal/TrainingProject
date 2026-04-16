from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MenuItem
from app.schemas.menu_item import MenuItemCreate


class ItemRepository:

    @staticmethod
    async def get_item_by_id(item_id: int, db:AsyncSession):
        item = await db.execute(select(MenuItem).where(MenuItem.item_id==item_id))
        item_model = item.scalar_one_or_none()
        return item_model

    @staticmethod
    async def add_item_to_db(item_payload:MenuItemCreate, db:AsyncSession):
        item_to_add = MenuItem(**item_payload)
        db.add(item_to_add)
        await db.commit()
        await db.refresh(item_to_add)
        return item_to_add