from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserUpdate, UserCreate


class UserRepository:

    @staticmethod
    async def get_user_by_id(user_id:int, db:AsyncSession) -> User:
        fetched_user = await db.execute(select(User).where(User.user_id==user_id))
        user_model = fetched_user.scalar_one_or_none()
        return user_model


    @staticmethod
    async def update_user(user, user_payload:UserUpdate, db:AsyncSession):
        for key, value in user_payload.items():
            setattr(user, key, value)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_email(email:str, db:AsyncSession) -> User:
        user_by_email = await db.execute(select(User).where(User.email == email))
        user_model = user_by_email.scalar_one_or_none()
        return user_model

    @staticmethod
    async def add_user(user_payload:UserCreate, db:AsyncSession) -> User:
        db_user = User(**user_payload)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user