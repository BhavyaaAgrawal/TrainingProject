from ast import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm import User
from app.dto.user import UserUpdate, UserCreate, UserLogin


class UserRepository:

    def __init__(self, session:AsyncSession):
        self.session = session
        
    async def get_user_by_id(self, user_id:int):
        fetched_user = await self.session.execute(select(User).where(User.user_id==user_id))
        user_model = fetched_user.scalar_one_or_none()
        return user_model

    async def reset_password(self, user, user_payload:UserLogin):
        for key, value in user_payload.items():
            setattr(user, key, value)
        await self.session.flush()
        await self.session.refresh(user)
        return user


    async def update_user(self, user, user_payload:UserUpdate):
        for key, value in user_payload.items():
            setattr(user, key, value)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_user_by_email(self, email:str) -> User:
        user_by_email = await self.session.execute(select(User).where(User.email == email))
        user_model = user_by_email.scalar_one_or_none()
        return user_model

    async def add_user(self, user_payload:UserCreate) -> User:
        self.session_user = User(**user_payload)
        self.session.add(self.session_user)
        await self.session.flush()
        await self.session.refresh(self.session_user)
        return self.session_user

    async def delete_user(self, user):
        await self.session.delete(user)
        await self.session.flush()
        return

    async def get_all_users(self) -> List[User]:
        all_users = await self.session.execute(select(User).order_by(User.user_id))
        all_users_model = all_users.scalars().all()
        return all_users_model