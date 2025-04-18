from fastapi import APIRouter, Depends, Request
from services import PatientService
from fastapi.responses import JSONResponse


patient_router:APIRouter = APIRouter(
    prefix='/patient-services',
    tags=['Patient Services']
)

__SERVIE__:PatientService = PatientService()

patient_router.dependencies= [Depends(__SERVIE__.checkService)]

from views import BaseResponse, GetAllPatientResponse, GET_ALL_PATIENTS_RES
from fastapi import Query
@patient_router.get(
    path='/patients',
    response_model=GetAllPatientResponse,
    status_code=200,
    description='Retrieve all pateints of a medical staff. (Authorization mandatory)',
    responses=GET_ALL_PATIENTS_RES
)
async def getAll(
    id:int=Depends(__SERVIE__.extractMID),
    page:int=Query(1, ge=1, description='page number')
):
    response:BaseResponse= await __SERVIE__.getAll(id=id, page=page)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )

from views import GetOnePatientResponse, GET_PATIENT_INFO_RES
@patient_router.get(
    path='/patient/{patient}',
    response_model=GetOnePatientResponse,
    status_code=200,
    description='Retrieve patient information. (Authorization mandatory)',
    responses=GET_PATIENT_INFO_RES
)
async def getOne(
    patient:int,
    id:int=Depends(__SERVIE__.extractMID)
)->BaseResponse:
    response:BaseResponse=await __SERVIE__.getOne(mid=id, pid=patient)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )

from views import CreatePatientRequest, CreatePatientResponse, CREATE_PATIENT_RES
@patient_router.post(
    path='/patient/new',
    status_code=201,
    response_model=CreatePatientResponse,
    responses=CREATE_PATIENT_RES
)
async def create(
    req:CreatePatientRequest,
    id:int=Depends(__SERVIE__.extractMID)
)->BaseResponse:
    response:BaseResponse=await __SERVIE__.create(id=id, data=req)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )

from views import UpdatePatientRequest, UpdatePtaitenResponse, UPDATE_PATIENT_RES
@patient_router.put(
    path='/patient/update',
    status_code=200,
    response_model=UpdatePtaitenResponse,
    responses=UPDATE_PATIENT_RES
)
async def update(
    req:UpdatePatientRequest,
    id:int=Depends(__SERVIE__.extractMID)
)->BaseResponse:
    response:BaseResponse=await __SERVIE__.update(id=id, data=req)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )

from views import DeletePatientRequest, DeletePatientResponse, DELETE_PATIENT_RES
@patient_router.delete(
    path='/patient/delete',
    status_code=200,
    response_model=DeletePatientResponse,
    responses=DELETE_PATIENT_RES
)
async def delete(
    req:DeletePatientRequest,
    id:int=Depends(__SERVIE__.extractMID)
)->BaseResponse:
    response:BaseResponse=await __SERVIE__.deletePatient(id=id, data=req)
    return JSONResponse(
        status_code=response.code,
        content=response.model_dump(exclude_none=True)
    )