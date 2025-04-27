from fastapi import APIRouter, Depends, Request
from services import AuthService
from fastapi.responses import JSONResponse


auth_router:APIRouter = APIRouter(
    prefix='/auth-service',
    tags=['Auth Services']
)

__SERVICE__:AuthService=AuthService()

auth_router.dependencies = [Depends(__SERVICE__.CheckService)]

from views import AuthRegisterResponse, REGISTER_RESPONSES, AuthRegisterRequest, BaseResponse
@auth_router.post(
    path='/register',
    response_model=AuthRegisterResponse,
    responses=REGISTER_RESPONSES,
    status_code=201
)
async def register(request:AuthRegisterRequest) -> BaseResponse:
    response= await __SERVICE__.register(data=request)
    return JSONResponse(status_code=response.code, content=response.model_dump())



from views import AuthLoginRequest, AuthLoginResponse, BaseResponse, LOGIN_RESPONSES
from middlewares import limiter
@auth_router.post(
    path='/login',
    status_code=200,
    response_model=AuthLoginResponse,
    responses=LOGIN_RESPONSES
)
# @limiter.limit('10/minute')
async def login(req:AuthLoginRequest, request:Request) -> BaseResponse:
    response= await __SERVICE__.login(data=req)
    return JSONResponse(status_code=response.code, content=response.model_dump(exclude_none=True))


from views import ForgetPasswordRequest, BaseResponse
@auth_router.post(
    path='/forgot-password',
    response_model=BaseResponse,
    status_code=200
)
async def forget_password(req:ForgetPasswordRequest):
    response= await __SERVICE__.forget_password(data=req)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )

from views import ResetPasswordRequest
@auth_router.post(
    path='/reset/{token}',
    response_model=BaseResponse,
    status_code=200
)
async def reset_password(token:str, req:ResetPasswordRequest):
    response= await __SERVICE__.reset_password(data=req, token=token)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )

from views import UnLockRequest
@auth_router.put(
    path='/account/unlock',
    response_model=BaseResponse,
    status_code=200
)
async def unlock_account(req:UnLockRequest):
    response= await __SERVICE__.unlock(data=req)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )
