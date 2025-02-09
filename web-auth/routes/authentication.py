from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from controllers import UserController

from sqlalchemy.ext.asyncio import AsyncSession
from core import GET_ENGINE

authentication:APIRouter=APIRouter(
    prefix='/auth/v1',
    tags=['Authentication']
)

from views import (
    RegisterRequest, 
    RegisterResponseBase,
    Register201,
    register_dump
)
@authentication.post(
    path='/register',
    description='Register new user in the system',
    status_code=201,
    response_model=Register201,
    responses=register_dump
)

async def register_endpoint(
    req:RegisterRequest,
    session:AsyncSession | None=Depends(GET_ENGINE)
)->RegisterResponseBase:
    response:RegisterResponseBase= await UserController.register(user=req, session=session)
    if not isinstance(response, Register201):
        return JSONResponse(status_code=response.code, content=response.model_dump())
    return response



from views import (
    LoginRequest,
    LoginResponseBase,
    Login200,
    login_dump
)

@authentication.post(
    path='/login',
    description='Login to the system using user credentials',
    status_code=200,
    response_model=Login200,
    responses=login_dump
)
async def login_endpoint(
    req:LoginRequest,
    session:AsyncSession=Depends(GET_ENGINE)
)->LoginResponseBase:
    response:LoginResponseBase=await UserController.login(credentials=req, session=session)
    if not isinstance(response, Login200):
        return JSONResponse(status_code=response.code, content=response.model_dump())
    return response