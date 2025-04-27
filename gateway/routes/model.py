from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.responses import JSONResponse
from services import ModelService
from views import BaseResponse

model_router:APIRouter=APIRouter(
    prefix='/model-services',
    tags=['Model']
)

__SERVICE__:ModelService=ModelService()
model_router.dependencies=[Depends(__SERVICE__.check_service)]

from views import DiagnoseRequest, fromData, DiagnoseResponse
@model_router.post(
    path='/diagnose',
    description='Glaucoma and severity diagnose from uploaded image/images',
    status_code=200,
    response_model=DiagnoseResponse
)
async def diagnose(
    req:DiagnoseRequest=Depends(fromData),
    octs:list[UploadFile]= File(...),
    sid:int=Depends(__SERVICE__.extractMID),
)->BaseResponse:
    res:BaseResponse = await __SERVICE__.diagnose(data=req, sid=sid, octs=octs)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

from views import StaffReportsResponse
@model_router.get(
    path='/reports/metadata',
    status_code=200,
    description='Retrieve all medical staff\'s reports metadata',
    response_model=StaffReportsResponse
)
async def reports_meta(
    sid:int=Depends(__SERVICE__.extractMID),
    page:int=Query(default=1, description='reports page', ge=1)
)-> BaseResponse:
    res:BaseResponse = await __SERVICE__.get_reports(page=page, sid=sid)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )


@model_router.get(
    path='/images/{image}',
    status_code=200,
    description='Retrive image stored on server',
)
async def get_image(
    image:str,
    sid:int=Depends(__SERVICE__.extractMID),
):
    res = await __SERVICE__.get_image(sid=sid, image=image)
    if isinstance(res, BaseResponse):
        return JSONResponse(
            status_code=res.code,
            content=res.model_dump(exclude_none=True)
        )
    return res