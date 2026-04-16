from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserUpdate
from app.services.user_service import add_user, validate_login_user, get_specific_user, updated_user, deleted_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login-user")
async def login_user(user: UserLogin, db:AsyncSession = Depends(get_db)):
    return await validate_login_user(user, db)


@router.get("/get-user",  response_model=UserResponse)
async def get_user(user_id: int, db:AsyncSession = Depends(get_db)):
    return await get_specific_user(user_id, db)


@router.post("/create-user")
async def create_user(user: UserCreate, db:AsyncSession = Depends(get_db)):
    user_payload = user.model_dump()
    return await add_user(user_payload, db)

@router.patch("/update-user")
async def update_user(user_id:int, user: UserUpdate, db:AsyncSession = Depends(get_db)):
    # dump or dict of input params body we are passing to this route point
    user_payload = user.model_dump()
    return await updated_user(user_id, user_payload, db)

@router.delete("/delete-user")
async def delete_user(user_id:int, db:AsyncSession = Depends(get_db)):
    return await deleted_user(user_id, db)