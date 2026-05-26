from fastapi import HTTPException
from app.dto.menu_item import MenuItemUpdate
from app.db.uow import UnitOfWork

class MenuItemService:
    def __init__(self, uow:UnitOfWork):
        self.uow=uow

    async def fetch_item(self, item_id:int):
        item = await self.uow.items.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"message": "Item fetched successfully", "data": [item]}

    async def create_item(self, item):
        item_data = item.model_dump(exclude_unset=True)
        await self.uow.items.add_item_to_db(item_data)
        return {"message": "Item created successfully", "data": []}

    async def updated_item(self, item_id:int, item_payload:MenuItemUpdate):
        #fetch item from db
        item = await self.uow.items.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        await self.uow.items.update_existing_item(item, item_payload)
        return {"message": "Item updated successfully", "data": []}

    async def get_all_menu_items(self):
        menu_items = await self.uow.items.get_all_menu_items()
        return {"message": "Menu items fetched successfully", "data": menu_items}

    async def deleted_item(self, item_id:int):
        item_exists = await self.uow.items.get_item_by_id(item_id)
        if not item_exists:
            raise HTTPException(status_code=404, detail="Item not found")
        await self.uow.items.delete_item(item_id)
        return {"message": "Item deleted successfully", "data": []}

    async def fetch_restaurant_items(self, restaurant_id:int):
        rest_data = await self.uow.items.fetch_restaurant_items(restaurant_id)
        if not rest_data:
            raise HTTPException(status_code=404, detail=f"No menu items found for restaurant id: {restaurant_id}")
        return {"message": f"Menu items fetched successfully for restaurant:{restaurant_id}", "data": rest_data}
