from fastapi import HTTPException
import logging
from app.core.security import hash_password, verify_password
from app.core.exceptions.domain import NotFoundError, IncorrectPasswordError, ConflictError
from app.core.exceptions import error_codes
from app.core.exceptions import error_messages

logger = logging.getLogger(__name__)

class UserService():
    def __init__(self,uow):
        self.uow = uow

    async def add_user(self, user_payload):
        """ This method will add a new user to system """
        user_with_same_email = await self.uow.users.get_user_by_email(user_payload['email'])
        if user_with_same_email:
            logger.error(f"Adding user with same email {user_payload['email']} failed")
            raise ConflictError(error_codes.EMAIL_ALREADY_EXISTS,
                                error_messages.EMAIL_ALREADY_EXISTS)
        user_payload['password'] = hash_password(user_payload['password'])
        await self.uow.users.add_user(user_payload)
        return {"message": "User added successfully"}
    
    
    async def validate_login_user(self, user_payload):
        """ This method will validate the login user """
        # fetch user from db
        user_model = await self.uow.users.get_user_by_email(user_payload.email)
        if user_model is None:
            raise NotFoundError(error_codes.USER_NOT_FOUND, error_messages.USER_NOT_FOUND)
        if not verify_password(user_payload.password, user_model.password):
            logger.error(f'User password is incorrect')
            raise IncorrectPasswordError(error_codes.INCORRECT_EMAIL_OR_PASSWORD, error_messages.INCORRECT_EMAIL_OR_PASSWORD)
        return {"message": "Login successful",
                'user_id': user_model.user_id}
    
    
    async def get_specific_user(self, user_id: int):
        """ This method will return a specific user wrt user_id from the db """
        user = await self.uow.users.get_user_by_id(user_id)
        if not user:
            raise NotFoundError(error_codes.USER_NOT_FOUND, error_messages.USER_NOT_FOUND)
        return {"message": "User fetched successfully", "data": user}
    
    
    async def updated_user(self, user_id, user_payload):
        """ This method will update user properties """
        user = await self.uow.users.get_user_by_id(user_id)
        if not user:
            raise NotFoundError(error_codes.USER_NOT_FOUND, error_messages.USER_NOT_FOUND)
        await self.uow.users.update_user(user, user_payload)
        return {"message": "User updated successfully"}
    
    
    async def deleted_user(self, user_id: int):
        """ This method will delete a user from the db  """
        user = await self.uow.users.get_user_by_id(user_id)
        if user is None:
            raise NotFoundError(error_codes.USER_NOT_FOUND, error_messages.USER_NOT_FOUND)
        await self.uow.users.delete_user(user)
        return {"message": "User deleted successfully"}
    
    async def reset_user_password(self, user_payload):
        user_email = user_payload.get('email')
        user_payload['password'] = hash_password(user_payload['password'])
        user = await self.uow.users.get_user_by_email(user_email)
        if not user:
            raise HTTPException(status_code=404, detail=f"User with email: {user_email} not found")
        await self.uow.users.reset_password(user, user_payload)
        return {"message": f"Password reset successful for user:{user_email}", "status": {"success":True}}
    
    async def get_all_users(self):
        all_users = await self.uow.users.get_all_users()
        if not all_users:
            raise NotFoundError(error_codes.USER_NOT_FOUND, error_messages.USER_NOT_FOUND)
        return all_users