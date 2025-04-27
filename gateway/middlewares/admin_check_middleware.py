from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import HTTPException

from services import AuthService

from views import (
    ServerSideErrorResponse, 
    UnauthorizedResponse, 
    VerifyTokenResponse, 
    VerifyTokenRequest, 
    ForbiddenResponse,
    BaseResponse
)

class AdminCheckMiddleware:
    @staticmethod
    async def dispatch(request:Request):
        __AUTHORIZATION__:AuthService=AuthService()
        try:
            #pre-flight request
            if request.method == "OPTIONS":
                return
            
            access_token:str = request.headers.get('authorization')

            #protected & no authorization header
            if not access_token:
                raise HTTPException(
                    status_code=UnauthorizedResponse().code,
                    detail=UnauthorizedResponse().model_dump(exclude_none=True)
                )
            
            access_token=access_token.split(' ')[-1]

            res:VerifyTokenResponse = await __AUTHORIZATION__.verify(data=VerifyTokenRequest(token=access_token))
            if not res.valid:
                raise HTTPException(
                    status_code=ForbiddenResponse().code,
                    detail=ForbiddenResponse().model_dump(exclude_none=True)
                )
            
            is_admin:BaseResponse = await __AUTHORIZATION__.is_admin(id=res.role)

            if is_admin.code != 200:
                raise HTTPException(
                    status_code=ForbiddenResponse().code,
                    detail=ForbiddenResponse().model_dump(exclude_none=True)
                )
        except Exception as e:
            print(f'[Gateway] - Admin middleware exception:\n{e}')

            if isinstance(e, HTTPException): raise e

            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump(exclude_none=True)
            )