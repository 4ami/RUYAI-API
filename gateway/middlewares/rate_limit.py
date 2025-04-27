from services import AuthService
from starlette.requests import Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address
from views import AuthLockRequest

limiter:Limiter = Limiter(key_func=get_remote_address)
_auth_service:AuthService = AuthService()

async def rate_limit_handler(req: Request, exc:RateLimitExceeded):
    if '/login' in req.url.path:
       return await _login_rate_limit(req=req, exc=exc)
    return await _rate_limit_handler(req=req, exc=exc)


async def _rate_limit_handler(req:Request, exc:RateLimitExceeded)-> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "code": 429,
            "message": "Too much requests, try again after few seconds"
        }
    )

async def _login_rate_limit(req:Request, exc:RateLimitExceeded) -> JSONResponse:
    try:
        json=await req.json()
        lock=await _auth_service.lock(data=AuthLockRequest(email=json.get('email')))
        if lock.get('code') == 404:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "message": 'Email/Password incorrect'
                }
            )
        
        if lock.get('code') not in [200, 409]:
            print(f'Lock unsuccessful response code: {lock.get('code')}')
            print(f'{lock.get('message')}')
            return JSONResponse(
                status_code=429,
                content={
                    "code": 429,
                    "message": "Too much requests, try again after few seconds"
                }
            )
        
        return JSONResponse(
            status_code=429,
            content={
                "code": 429,
                "message": 'Account is locked. We send you an email to re-activate your account.'
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=429,
            content={
                "code": 429,
                "message": "3s"
            }
        )
