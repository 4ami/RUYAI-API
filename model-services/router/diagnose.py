from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from core import GET_ENGINE

diagnosis_router:APIRouter=APIRouter(
    prefix='/diagnose/v1',
    tags=['Diagnosis Model']
)



from view import fromData, DiagnoseRequest
from middleware import validate_oct_middleware
from view import Diagnosis200, ServerSideErrorResponse, ResponseBaseModel
from controller import ImageSetController, DiagnoseReportController

@diagnosis_router.post(
    path='/',
    description='Upload OCT and diagnose it system',
    response_model=Diagnosis200,
    status_code=200
)
async def diagnose(
    req:DiagnoseRequest=Depends(fromData),
    oct:list[UploadFile] = Depends(validate_oct_middleware),
    session:AsyncSession|None=Depends(GET_ENGINE)
):
    report_id:int = await DiagnoseReportController.create_report(data=req, session=session)
    if not report_id:
        return JSONResponse(
            status_code=ServerSideErrorResponse().code,
            content=ServerSideErrorResponse().model_dump()
        )
    response:ResponseBaseModel= await ImageSetController.add(report_id=report_id, octs=oct, session=session)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )
