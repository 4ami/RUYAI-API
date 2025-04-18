from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from views import ServerSideErrorResponse

class ServerErrorMiddlewareHandler(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            print(f'[Gateway] - Error Middleware:\n{e}')
            return JSONResponse(
                status_code= ServerSideErrorResponse().code,
                content=ServerSideErrorResponse().model_dump(exclude_none=True)
            )