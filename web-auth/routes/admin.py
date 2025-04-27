from fastapi import APIRouter, Depends
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

admin_router:APIRouter = APIRouter(
    prefix='/admin',
    tags=['Admin Services']
)


from controllers import UserController
from views import (
    AdminUpdateUserRequest, 
    AdminUpdateUserResponse,
    PendingAccountsResponse
)


@admin_router.get(
    path='/accounts/pendings',
    status_code=200,
    response_model=PendingAccountsResponse
)
async def get_pendings(
    session: AsyncSession | None = Depends(GET_ENGINE)
):
    res = await UserController.get_pendings(session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

@admin_router.put(
    path='/update/user',
    response_model=AdminUpdateUserResponse,
    status_code=200
)
async def update_user(
    req:AdminUpdateUserRequest,
    session: AsyncSession | None = Depends(GET_ENGINE)
):
    res = await UserController.edit_user_admin(data=req, session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )