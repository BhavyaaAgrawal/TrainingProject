from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models import User
from app.repository.user_repository import UserRepository


async def add_user(user_payload, db: AsyncSession):
    """ This method will add a new user to system """
    print(user_payload['password'])
    # check if user with provided email already exists, if yes raise validation error else add new user
    user_with_same_email = await UserRepository.get_user_by_email(user_payload['email'], db)
    if user_with_same_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_payload['password'] = hash_password(user_payload['password'])
    await UserRepository.add_user(user_payload, db)
    return {"message": "User added successfully"}


async def validate_login_user(user_payload, db: AsyncSession):
    """ This method will validate the login user """
    # fetch user from db
    user_from_db = await db.execute(select(User).where(User.email == user_payload.email))
    user_model = user_from_db.scalar_one_or_none()
    if user_model is None:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(user_payload.password, user_model.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"message": "Login successful",
            'user_id': user_model.user_id}


async def get_specific_user(user_id: int, db: AsyncSession):
    """ This method will return a specific user wrt user_id from the db """
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def updated_user(user_id, user_payload, db: AsyncSession):
    """ This method will update user properties """
    print(user_payload)
    # fetch respective user on the basis of user_id
    user = await UserRepository.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await UserRepository.update_user(user, user_payload, db)
    return {"message": "User updated successfully"}


async def deleted_user(user_id: int, db: AsyncSession):
    """ This method will delete a user from the db  """
    user = await db.execute(select(User).where(User.user_id == user_id))
    user_response = user.scalar_one_or_none()
    if user_response is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user_response)
    await db.commit()
    return {"message": "User deleted successfully"}