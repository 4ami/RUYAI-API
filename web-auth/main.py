from fastapi import FastAPI
from fastapi.responses import JSONResponse
from utility import TokenHelper

service = FastAPI(
    title='Web-Authentication & Authorization Service',
    summary='Service handels all A&A-related services'
)

@service.get('/ping')
def ping(): 
    return JSONResponse(content={'message': 'pong', 'health': 'Running', 'code': 200}, status_code=200)

from routes import authentication, security

service.include_router(router=authentication)
service.include_router(router=security)