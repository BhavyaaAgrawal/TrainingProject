from fastapi import APIRouter, Depends
from app.services.item_service import MenuItemService
from app.dto.menu_item import MenuItemCreate, MenuItemUpdate
from app.dependencies import menu_item_service

router = APIRouter(prefix="/menu-items", tags=["Items"])

@router.get("/get-item")
async def get_item(item_id: int,svc:MenuItemService=Depends(menu_item_service)):
    return await svc.fetch_item(item_id)

@router.get('/get-restaurant-menu-items')
async def get_restaurant_items(restaurant_id: int, svc:MenuItemService=Depends(menu_item_service)):
    rest_data = await svc.fetch_restaurant_items(restaurant_id)
    return rest_data


@router.post("/add-item")
async def add_item(item: MenuItemCreate,svc:MenuItemService=Depends(menu_item_service)):
    return await svc.create_item(item)

@router.put("/update-item")
async def update_item(item_id:int, item: MenuItemUpdate, svc:MenuItemService=Depends(menu_item_service)):
    item_payload = item.model_dump(exclude_unset=True)
    return await svc.updated_item(item_id, item_payload)

@router.get('/get-all-items')
async def get_all_items(svc:MenuItemService=Depends(menu_item_service)):
    return await svc.get_all_menu_items()

@router.delete("/delete-item")
async def delete_item(item_id:int,svc:MenuItemService=Depends(menu_item_service)):
    return await svc.deleted_item(item_id)
