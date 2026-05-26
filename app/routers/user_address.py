from fastapi import APIRouter, Depends
from app.dto.user_address import AddressCreate, AddressUpdate, AddressResponse
from app.services.user_address import UserAddressService
from app.dependencies import get_user_address_service

router = APIRouter(prefix="/user-address", tags=["User-Address"])

@router.post("/add-address")
# pass the instance of useraddressservice in svc from here and it will take depends as parameter that will be stored in uow variable in __init__
async def add_user(address: AddressCreate, svc:UserAddressService = Depends(get_user_address_service)):
    address_payload = address.model_dump(exclude_unset=True, exclude_none=True)
    return await svc.add_address(address_payload)

@router.get('/get-address')
async def get_address(user_id:int, svc:UserAddressService = Depends(get_user_address_service)):
    print('svc======', svc)
    # svc here tells get_adress that u need to call UserAdressService using it and it depends on uow directly passed in
    # get_user_address_service from dependencies file feeding __init__ method of UserAddressService class
    return await svc.get_address_for_user(user_id)

@router.patch('/update-address')
async def update_user_address(user_id:int, address:AddressUpdate, svc:UserAddressService = Depends(get_user_address_service)):
    # to avoid unprovided values to be updated by none, use exclude_unset=True
    address_payload = address.model_dump(exclude_unset=True)
    return await svc.updated_user_address(user_id, address_payload)

@router.delete('/delete-address')
async def delete_user_address(user_id:int, svc:UserAddressService = Depends(get_user_address_service)):
    return await svc.delete_user_address(user_id)
