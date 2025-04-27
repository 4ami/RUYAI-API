from fastapi import APIRouter, Depends
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

role_router:APIRouter = APIRouter(
    prefix='/role',
    tags=['User Roles']
)


from controllers import RoleController
from views import AllowedRolesResponse

@role_router.get(
    path='/allowed',
    description='Allowed roles for registeration form',
    response_model=AllowedRolesResponse,
    status_code=200
)
async def get_allowed_roles(
    session:AsyncSession|None= Depends(GET_ENGINE)
):
    res:AllowedRolesResponse=await RoleController.get_allowed_roles(session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )