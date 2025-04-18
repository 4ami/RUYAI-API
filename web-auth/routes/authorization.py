from fastapi import APIRouter
from fastapi.responses import JSONResponse

authorization:APIRouter=APIRouter(
    prefix='/authorization',
    tags=['Authorization']
)



from views import VerifyTokenRequest, VerifyTokenResponse
from controllers import AuthorizationController
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