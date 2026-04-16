from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from app.db.database import get_db
from app.models import User
from app.models.user import User
from app.models.menu_items import MenuItem
from app.schemas import menu_item
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.menu_item import MenuItemCreate
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password, verify_password
from app.routers import user, items

app=FastAPI()


# utilising user from routes, all the routes defined inside users route will come as we have included routes within context of app
app.include_router(user.router)

app.include_router(items.router)

@app.get("/")
async def root():
    # return {"message": "Hello World"}
    return RedirectResponse(url="/docs")

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# @app.post("/users/")
# async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     data = user.model_dump()
#     print(data['password'])
#     data['password'] = hash_password(data['password'])
#     db_user = User(**data)
#     db.add(db_user)
#     await db.commit()
#     await db.refresh(db_user)
#     return db_user


# @app.post("/login")
# async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
#     print(user_data.model_dump())
#     result = await db.execute(select(User).where(User.email == user_data.email))
#     # to show response is of type ChunkedIteratorResult
#     # result.user_id
#     # correct method is
#     user = result.scalar_one_or_none()
#     if not verify_password(user_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     return {"message": "Login successful",
#             'user_id': user.user_id}


# @app.get("/users/{user_id}", response_model=UserResponse)
# async def read_user(user_id: int,  db: AsyncSession = Depends(get_db)):
#     user_query = await db.execute(select(User).where(User.user_id == user_id))
#     # now user_query will be returned in sync with UserResponse ie as it inherits UserBase so we will only get name, email, password
#     user_response = user_query.scalar_one_or_none()
#     if user_response is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user_response


# @app.post("/menu_items/")
# async def create_menu_items(menu_item: MenuItemCreate, db: AsyncSession = Depends(get_db)):
#     db_menu_item = MenuItem(**menu_item.model_dump())
#     db.add(db_menu_item)
#     await db.commit()
#     await db.refresh(db_menu_item)
#     return db_menu_item

# @app.post("/restaurants/")
# async def create_restaurants(restaurant: RestaurantCreate, db: AsyncSession = Depends(get_db)):
#     db_restaurant = Restaurant(**restaurant.model_dump())
#     db.add(db_restaurant)
#     await db.commit()
#     await db.refresh(db_restaurant)
#     return db_restaurant