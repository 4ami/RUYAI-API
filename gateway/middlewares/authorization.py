from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from views import (
    ServerSideErrorResponse, 
    UnauthorizedResponse, 
    ForbiddenResponse,
    VerifyTokenRequest,
    VerifyTokenResponse
)
from services import AuthService
import re

class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protect:list[str]=[], skip:list[str]=[]):
        super().__init__(app)
        self.protect:list[str]= protect
        self.skip:list[str]=skip
        self.__AUTHORIZATION__:AuthService=AuthService()

    async def dispatch(self, request, call_next):
        try:
            #pre-flight request
            if request.method == "OPTIONS":
                return await call_next(request)
            
            #if skipped
            if request.url.path in self.skip:
                return await call_next(request)

            #not protected
            if not re.search('|'.join(map(re.escape, self.protect)), request.url.path):
                return await call_next(request)

            access_token:str = request.headers.get('authorization')

            #protected & no authorization header
            if not access_token:
                return JSONResponse(
                    status_code=UnauthorizedResponse().code,
                    content=UnauthorizedResponse().model_dump(exclude_none=True)
                )
            
            access_token=access_token.split(' ')[-1]

            #protected & invalid token
            res:VerifyTokenResponse = await self.__AUTHORIZATION__.verify(data=VerifyTokenRequest(token=access_token))
            if not res.valid:
                return JSONResponse(
                    status_code=ForbiddenResponse().code,
                    content=ForbiddenResponse().model_dump(exclude_none=True)
                )
            
            #protected & valid token
            request.state.id=res.id
            return await call_next(request)
        except Exception as e:
            print(f'[Gateway] - Authorization middleware exception:\n{e}')
            return JSONResponse(
                status_code=ServerSideErrorResponse().code,
                content=ServerSideErrorResponse().model_dump(exclude_none=True)
            )