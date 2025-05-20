from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession

authorization:APIRouter=APIRouter(
    prefix='/authorization',
    tags=['Authorization']
)



from views import VerifyTokenRequest, VerifyTokenResponse, IsAdminResponse
from controllers import AuthorizationController, RoleController
@authorization.post(
    path='/verify',
    description='Verify access token.',
    response_model=VerifyTokenResponse,
    status_code=200
)
async def verify(req:VerifyTokenRequest)->VerifyTokenResponse:
    res:VerifyTokenResponse=await AuthorizationController.verify(data=req)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

@authorization.get(
    path='/admin/role/{id}',
    description='Check if this was admin role id',
    status_code=200
)
async def is_admin(id:int, session:AsyncSession|None=Depends(GET_ENGINE)):
    isAdmin:bool = await RoleController.is_admin(role=id, session=session)
    res:IsAdminResponse=IsAdminResponse(
        code=200 if isAdmin else 403,
        message=f'The given role {'is ADMIN' if isAdmin else 'NOT ADMIN'}'
    )
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump()
    )

from views import GenerateApiKeyResponse, GenerateApiKeyRequest
from controllers import ApiKeysController
@authorization.post(
    path='/api-key/generate',
    description='Generate Api Key for IT Staff',
    status_code=201,
    response_model=GenerateApiKeyResponse
)
async def generate(req:GenerateApiKeyRequest, session:AsyncSession|None=Depends(GET_ENGINE)):
    res = await ApiKeysController.generate(id=req.id, session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )