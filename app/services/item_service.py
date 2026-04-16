from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.menu_items_repository import ItemRepository


async def fetch_item(item_id:int, db:AsyncSession):
    item = await ItemRepository.get_item_by_id(item_id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

async def create_item(item, db:AsyncSession):
    item_data = item.model_dump()
    return await ItemRepository.add_item_to_db(item_data, db)
