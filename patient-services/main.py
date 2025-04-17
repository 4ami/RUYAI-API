from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

app:FastAPI=FastAPI(
    title='Patient Managment Services',
    summary='Service manages patients information',
)

from fastapi import Query
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession

@app.get('/')
def ping(): return JSONResponse(content={'message': 'pong', 'health': 'Running', 'code': 200}, status_code=200)

from controller import PatientGET, PatientPOST, PatientInfoPUT
from view import (
    BaseResponse,
    GetAllResponse,
    GetOneResponse,
    GET_ONE_RESPONSES,
    GET_ALL_RESPONSES,
    CreatePatientRequest,
    CreatePatientResponse,
    UpdatePatientInfoRequest,
    UpdatedPatientInfoResponse,
    UPDATE_PATIENT_INFO_RESPONSES
)
@app.get(
    path='/patients/{medical_staff_id}',
    status_code=200,
    description='Retrieve all hospital patients',
    response_model=GetAllResponse,
    responses=GET_ALL_RESPONSES
)
async def get(
    medical_staff_id:int, 
    page:int=Query(1, ge=1, description='page number'), 
    session: AsyncSession | None = Depends(GET_ENGINE)
)-> BaseResponse:
    patients:BaseResponse=await PatientGET.all(medical_staff_id=medical_staff_id, page=page, session=session)
    
    if not isinstance(patients, GetAllResponse): 
        return JSONResponse(
            status_code=patients.code,
            content=patients.model_dump()
        )

    return patients



@app.get(
    path='/patients/{medical_staff_id}/{patient_id}',
    status_code=200,
    description='Retrieve specific patient information',
    response_model=GetOneResponse,
    responses=GET_ONE_RESPONSES
)
async def get_one(
    medical_staff_id:int,
    patient_id:int,
    session: AsyncSession | None = Depends(GET_ENGINE)
) -> BaseResponse:
    patient:BaseResponse=await PatientGET.one(medical_staff_id=medical_staff_id, patient_id=patient_id, session=session)

    return JSONResponse(
        status_code=patient.code,
        content=patient.model_dump(exclude_none=True)
    )

@app.post(
    path='/patient',
    description='Create new patient',
    status_code=201,
    response_model=CreatePatientResponse
)
async def create(
    req:CreatePatientRequest,
    session:AsyncSession|None=Depends(GET_ENGINE)
)->BaseResponse:
    res:BaseResponse=await PatientPOST.create(data=req, session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )


@app.put(
    path='/patient/update',
    description='Update patient information',
    status_code=200,
    response_model=UpdatedPatientInfoResponse,
    responses=UPDATE_PATIENT_INFO_RESPONSES
)
async def update(
    req:UpdatePatientInfoRequest,
    session:AsyncSession|None=Depends(GET_ENGINE)
)->BaseResponse:
    res:BaseResponse = await PatientInfoPUT.update(data=req, session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )


from view import DeletePatientRequest, DeleteResponse
from controller import DeletePatientController
@app.delete(
    path='/patient/delete',
    description='Delete specific patient',
    status_code=200,
    response_model=DeleteResponse
)
async def delete(
    req:DeletePatientRequest,
    session:AsyncSession|None=Depends(GET_ENGINE)
)->BaseResponse:
    res:BaseResponse = await DeletePatientController.delete(data=req, session=session)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )