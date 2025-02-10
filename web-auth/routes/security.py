from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

security:APIRouter=APIRouter(
    prefix='/security-measure',
    tags=['Security Measures']
)

from sqlalchemy.ext.asyncio import AsyncSession
from core import GET_ENGINE


from controllers import SecurityController

from views import (
    LockRequest,
    LockBaseResponse,
    Lock200,
    lock_dump
)

@security.put(
    path='/lock',
    description='Security measure to lock account due suspicious activity or rate-limiting.',
    status_code=200,
    response_model=Lock200,
    responses=lock_dump
)
async def lock_endpoint(
    req:LockRequest,
    session:AsyncSession | None=Depends(GET_ENGINE)
):
    response:LockBaseResponse=await SecurityController.lock_account(inf=req, session=session)
    if not isinstance(response, Lock200):
        return JSONResponse(status_code=response.code, content=response.model_dump())
    return response


from views import (
    UnLockRequest,
    UnLockBaseResponse,
    UnLock200,
    unlock_dump
)

@security.put(
    path='/unlock',
    description='Security measure to unlock account after verifing the real user',
    status_code=200,
    response_model=UnLock200,
    responses=unlock_dump
)
async def unlock_endpoint(
    req:UnLockRequest,
    session:AsyncSession | None=Depends(GET_ENGINE)
):
    res:UnLockBaseResponse=await SecurityController.unlock(inf=req, session=session)
    if not isinstance(res, UnLock200):
        return JSONResponse(status_code=res.code, content=res.model_dump())
    return res