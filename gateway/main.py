from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from middlewares import(
    limiter, 
    rate_limit_handler, 
    ServerErrorMiddlewareHandler,
    AuthorizationMiddleware,
)
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware

from utility import PROTECTED, SKIPPED

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
gateway.add_middleware(AuthorizationMiddleware, protect=PROTECTED, skip=SKIPPED)

gateway.state.limiter=limiter
gateway.add_middleware(SlowAPIMiddleware)
gateway.add_exception_handler(429, rate_limit_handler)

@gateway.exception_handler(HTTPException)
async def custom_http_exception(req:Request, ex:HTTPException):
    return JSONResponse(status_code=ex.status_code, content=ex.detail)

@gateway.get(
    '/ping',
    description='Health check',
    tags=['Default Gateway Endpoint'],
    status_code=200,
)
def ping(): 
    return JSONResponse(content={'message': 'pong', 'health': 'Running', 'code': 200})

@gateway.get(
    path='/public/images/{resource}',
    description='Get Public Resource',
    status_code=200,
    tags=['Default Gateway Endpoint']
)
async def get_resource(resource:str):
    return FileResponse(path=f'static/public/images/{resource}', media_type='image/png')


from routes import auth_router, patient_router, model_router, reports_router, feedback_router, metadata_router, admin_router
gateway.include_router(router=auth_router)

gateway.include_router(router=patient_router)

gateway.include_router(router=model_router)

gateway.include_router(router=reports_router)

gateway.include_router(router=feedback_router)

gateway.include_router(router=metadata_router)

gateway.include_router(router=admin_router)