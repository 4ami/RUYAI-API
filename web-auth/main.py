from fastapi import FastAPI
from fastapi.responses import JSONResponse

service = FastAPI(
    title='Web-Authentication & Authorization Service',
    summary='Service handels all A&A-related services'
)

@service.get('/ping')
def ping(): 
    return JSONResponse(content={'message': 'pong', 'health': 'Running', 'code': 200}, status_code=200)

from routes import authentication, authorization, security, role_router, admin_router

service.include_router(router=authentication)
service.include_router(router=security)
service.include_router(router=authorization)
service.include_router(router=role_router)
service.include_router(router=admin_router)