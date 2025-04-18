from fastapi import FastAPI
from fastapi.responses import JSONResponse
from middlewares import(
    limiter, 
    rate_limit_handler, 
    ServerErrorMiddlewareHandler,
    AuthorizationMiddleware
)
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from utility import PROTECTED

gateway:FastAPI=FastAPI(
    title='Ruy\'AI API Gateway',
    description='Aggregate user requests to the right service and forward back the responses to the client side',
    root_path='/gateway',
)

gateway.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

gateway.add_middleware(ServerErrorMiddlewareHandler)
gateway.add_middleware(AuthorizationMiddleware, protect=PROTECTED)

gateway.state.limiter=limiter
gateway.add_middleware(SlowAPIMiddleware)
gateway.add_exception_handler(429, rate_limit_handler)

# gateway.add_middleware(AuthorizationMiddleware, protect=['/gateway/ping'])
@gateway.get(
    '/ping',
    description='Health check',
    tags=['Default Gateway Endpoint'],
    status_code=200,
)
def ping(): 
    return JSONResponse(content={'message': 'pong', 'health': 'Running', 'code': 200})

from routes import auth_router, patient_router
gateway.include_router(router=auth_router)

gateway.include_router(router=patient_router)