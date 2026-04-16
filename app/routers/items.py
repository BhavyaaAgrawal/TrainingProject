from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.item_service import fetch_item
from app.schemas.menu_item import MenuItemCreate
from app.services.item_service import create_item

router = APIRouter(prefix="/menu-items", tags=["Items"])


@router.get("/get-item")
async def get_item(item_id: int, db:AsyncSession=Depends(get_db)):
    return await fetch_item(item_id, db)

@router.post("/add-item")
async def add_item(item: MenuItemCreate, db:AsyncSession=Depends(get_db)):
    return await create_item(item, db)
