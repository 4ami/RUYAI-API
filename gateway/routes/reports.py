from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
import asyncio

reports_router:APIRouter=APIRouter(
    prefix='/reporting-service',
    tags=['Reprots']
)

from services import ModelService, PatientService

__PATIENT__:PatientService=PatientService()
__MODEL__:ModelService=ModelService()

reports_router.dependencies=[Depends(__PATIENT__.checkService), Depends(__MODEL__.check_service)]

from views import BaseResponse, ReportResponse, GetOnePatientResponse

@reports_router.get(
    path='/report/{rid}/patient/{pid}',
    description='Get patient full report information',
    status_code=200,
    response_model=ReportResponse
)
async def patient_report(
    rid:int,
    pid:int,
    sid:int=Depends(__MODEL__.extractMID),
)->BaseResponse:
    patient_report_task= __PATIENT__.getOne(mid=sid, pid=pid)
    diagnose_report_task= __MODEL__.report(rid=rid, sid=sid, pid=pid)

    patient, diagnose = await asyncio.gather(patient_report_task, diagnose_report_task)

    if patient.code != 200:
        return JSONResponse(status_code=patient.code, content=patient.model_dump(exclude_none=True))
    
    if not diagnose:
        return JSONResponse(status_code=diagnose.code, content=diagnose.model_dump(exclude_none=True))
    
    return JSONResponse(
        status_code=200,
        content= ReportResponse(
            code= 200, 
            message='Report information gathered successfully',
            patient_information=patient.patient, 
            report=diagnose.model_dump()
        ).model_dump(exclude_none=True)
    )

