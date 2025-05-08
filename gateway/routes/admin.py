from fastapi import APIRouter, Depends, Request, Query
from services import AuthService
from fastapi.responses import JSONResponse
from views import BaseResponse
from middlewares import AdminCheckMiddleware
admin_router:APIRouter=APIRouter(
    prefix='/admin-services',
    tags=['Admin']
)

__AUTH__:AuthService = AuthService()

admin_router.dependencies= [Depends(__AUTH__.CheckService), Depends(AdminCheckMiddleware.dispatch)]


from views import PendingAccountsResponse
@admin_router.get(
    path='/accounts/pending',
    status_code=200,
    response_model=PendingAccountsResponse
)
async def get_pendings():
    res = await __AUTH__.get_pendings()
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

from views import UserAccountsResponse
@admin_router.get(
    path='/accounts',
    status_code=200,
    response_model=UserAccountsResponse
)
async def get_accounts(page:int=Query(1, ge=1)):
    res = await __AUTH__.get_users(page=page)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

from views import UpdateUserByAdminRequest, UpdatedUserInformationByAdmin
@admin_router.put(
    path='/update/user',
    status_code=200,
    response_model=UpdatedUserInformationByAdmin
)
async def put_user(req:UpdateUserByAdminRequest):
    res = await __AUTH__.admin_put_user(data=req)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )