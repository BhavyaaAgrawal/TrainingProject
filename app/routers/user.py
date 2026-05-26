from fastapi import APIRouter, Depends
from app.dto.user import UserCreate, UserLogin, UserUpdate
from app.services.user_service import UserService
from app.core.logger import setup_logger
from app.dependencies import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login-user")
async def login_user(user: UserLogin,svc:UserService=Depends(user_service)):
    logger = setup_logger()
    logger.info('Checking user logged in feature')
    return await svc.validate_login_user(user)


@router.get("/get-user")
async def get_user(user_id: int,svc:UserService=Depends(user_service)):
    return await svc.get_specific_user(user_id)


@router.post("/create-user")
async def create_user(user: UserCreate, svc:UserService=Depends(user_service)):
    user_payload = user.model_dump(exclude_unset=True, exclude_none=True)
    return await svc.add_user(user_payload)

@router.patch("/update-user")
async def update_user(user_id:int, user: UserUpdate,svc:UserService=Depends(user_service)):
    # dump or dict of input params body we are passing to this route point
    user_payload = user.model_dump(exclude_unset=True, exclude_none=True)
    return await svc.updated_user(user_id, user_payload)

@router.post('/reset-password')
async def reset_password(user_payload:UserLogin, svc:UserService=Depends(user_service)):
    user_payload = user_payload.model_dump(exclude_unset=True, exclude_none=True)
    return await svc.reset_user_password(user_payload)

@router.delete("/delete-user")
async def delete_user(user_id:int,svc:UserService=Depends(user_service)):
    return await svc.deleted_user(user_id)

@router.get("/get-all-users")
async def get_all_user(svc:UserService=Depends(user_service)):
    return await svc.get_all_users()
