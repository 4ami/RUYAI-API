from .base_service import BaseService
from utility import AVAILABLE_SERVICES
from views import (
    BaseResponse,
    AuthRegisterRequest, 
    AuthRegisterResponse,
    AuthLoginRequest,
    AuthLoginResponse,
    AuthLockRequest
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
            raise HTTPException(status_code=response.status_code, detail=json)
        return AuthRegisterResponse(code=json['code'], message=json['message'])
    
    async def login(self, data:AuthLoginRequest) -> BaseResponse:
        response=await self.post(endpoint=os.getenv('AUTH_LOG'), data= data)
        json=response.json()
        if response.status_code == 422:
            from fastapi.exceptions import HTTPException
            raise HTTPException(status_code=response.status_code, detail=json)
        return AuthLoginResponse(
            code=json['code'],
            message=json['message'],
            token=json.get('token'),
            ref_token=json.get('ref_token'),
            type=json.get('type'),
            loc=json.get('loc')
        )
    
    async def lock(self, data:AuthLockRequest):
        print(data)
        response=await self.put(endpoint=os.getenv('AUTH_SEC_LOCK'), data=data)
        return response.json()

    async def unlock(self): pass