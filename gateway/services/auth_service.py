from .base_service import BaseService
from utility import AVAILABLE_SERVICES
from views import (
    BaseResponse,
    AuthRegisterRequest, 
    AuthRegisterResponse,
    AuthLoginRequest,
    AuthLoginResponse,
    AuthLockRequest,
    VerifyTokenRequest,
    VerifyTokenResponse,
    ForgetPasswordRequest,
    ResetPasswordRequest,
    AvailableRoles,
    PendingAccountsResponse,
    UpdatedUserInformationByAdmin,
    UpdateUserByAdminRequest,
    UnLockRequest
)

from dotenv import load_dotenv
import os

load_dotenv()

class AuthService(BaseService):
    
    def __init__(self):
        super().__init__(service=AVAILABLE_SERVICES.AUTH.value)
    
    async def CheckService(self) -> None:
        unavailable:AuthRegisterResponse=AuthRegisterResponse(code=503, message='Auth service is currently unavailable')
        try:
            from fastapi import HTTPException
            response=await self.get(endpoint='/ping')
            if response.status_code != 200: 
                raise HTTPException(status_code=503, detail=unavailable.model_dump())
        except Exception as e:
            raise HTTPException(status_code=503, detail=unavailable.model_dump())

    async def register(self, data:AuthRegisterRequest) -> BaseResponse:
        response= await self.post(endpoint=os.getenv('AUTH_REG'), data=data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return AuthRegisterResponse(code=json['code'], message=json['message'])
    
    async def login(self, data:AuthLoginRequest) -> BaseResponse:
        response=await self.post(endpoint=os.getenv('AUTH_LOG'), data= data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return AuthLoginResponse(
            code=json['code'],
            message=json['message'],
            token=json.get('token'),
            ref_token=json.get('ref_token'),
            type=json.get('type'),
            loc=json.get('loc')
        )
    
    async def lock(self, data:AuthLockRequest):
        response=await self.put(endpoint=os.getenv('AUTH_SEC_LOCK'), data=data)
        return response.json()

    async def unlock(self, data:UnLockRequest):
        response=await self.put(endpoint=os.getenv('AUTH_SEC_UNLOCK'), data=data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return BaseResponse(**json)

    async def verify(self, data:VerifyTokenRequest)->VerifyTokenResponse:
        response=await self.post(endpoint=os.getenv('AUTH_VER'), data=data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return VerifyTokenResponse(
            code=json['code'],
            message=json['message'],
            valid=json.get('valid'),
            id=json.get('id'),
            full_name=json.get('full_name'),
            role=json.get('role'),
        )
    
    async def forget_password(self, data:ForgetPasswordRequest)->BaseResponse:
        response = await self.post(endpoint=os.getenv('AUTH_FOG'), data=data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return BaseResponse(**json)
    
    async def reset_password(self, data:ResetPasswordRequest, token:str)->BaseResponse:
        endpoint:str = os.getenv('AUTH_RES').format(token=token)
        response=await self.post(endpoint=endpoint, data=data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return BaseResponse(**json)
    
    async def get_roles(self):
        response=await self.get(endpoint=os.getenv('METADATA_ROLES'))
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return AvailableRoles(**json)
    
    async def is_admin(self, id:int):
        endpoint:str=os.getenv('AUTH_ADM').format(id=id)
        response=await self.get(endpoint=endpoint)
        json=response.json()
        return BaseResponse(**json)
    
    async def get_pendings(self):
        response=await self.get(endpoint=os.getenv('ADMIN_GET_PENDINGS'))
        json=response.json()
        return PendingAccountsResponse(**json)
    
    async def admin_put_user(self, data:UpdateUserByAdminRequest):
        endpoint:str=os.getenv('ADMIN_PUT_USER')
        response=await self.put(endpoint=endpoint, data=data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json['detail'])
        return UpdatedUserInformationByAdmin(**json)