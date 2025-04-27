from .base_service import BaseService
from utility import AVAILABLE_SERVICES
from fastapi.exceptions import HTTPException
from fastapi.requests import Request


from dotenv import load_dotenv
import os
load_dotenv()

from views import (
    BaseResponse,
    ForbiddenResponse,
    ServerSideErrorResponse,
    GetAllPatientResponse,
    PatientInformation,
    GetOnePatientResponse,
    CreatePatientRequest,
    CreatePatientResponse,
    InternalCreatePatientRequest,
    UpdatePatientRequest,
    InternalUpdatePatientRequest,
    UpdatePtaitenResponse,
    DeletePatientRequest,
    InternalDeletePatientRequest,
    DeletePatientResponse
)


class PatientService(BaseService):
    def __init__(self):
        super().__init__(service=AVAILABLE_SERVICES.PATIENT)
    
    async def checkService(self)-> None:
        unavailable_service:BaseResponse = BaseResponse(
            code=503,
            message='Patient service is currently unavailable'
        )
        try:
            res=await self.get(endpoint='/ping')
            if res.status_code != 200:
                raise HTTPException(
                    status_code=unavailable_service.code,
                    detail=unavailable_service.model_dump()
                )
        except Exception as e:
            print(f'Patient service exception:\n{e}')
            raise HTTPException(
                    status_code=ServerSideErrorResponse().code,
                    detail=ServerSideErrorResponse().model_dump()
                )
    
    async def extractMID(self, req:Request)->int:
        if not hasattr(req.state, 'id'):
            raise HTTPException(
                status_code=ForbiddenResponse().code,
                detail=ForbiddenResponse().model_dump()
            )
        return req.state.id
    
    async def getAll(self, id:int, page:int)->BaseResponse:
        try:
            if not id: return ForbiddenResponse()
            endpoint:str=os.getenv('PATIENT_GET_ALL').format(id=id)
            res=await self.get(endpoint=endpoint, params={'page':page})
            json=res.json()
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            patients= json.get('patients', [])
            patients= [PatientInformation(**p) for p in patients]
            return GetAllPatientResponse(
                code=json.get('code'),
                message=json.get('message'),
                patients=patients
            )
        except Exception as e:
            print(f'Patient service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            return ServerSideErrorResponse()

    async def getOne(self, mid:int, pid:int)->BaseResponse:
        try:
            if not mid: return ForbiddenResponse()
            endpoint:str=os.getenv('PATIENT_GET_ONE').format(id=mid, patient=pid)
            res=await self.get(endpoint=endpoint)
            json=res.json()
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            return GetOnePatientResponse(
                code=json.get('code'),
                message=json.get('message'),
                patient=json.get('patient')
            )
        except Exception as e:
            print(f'Patient service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            return ServerSideErrorResponse()
        
    async def create(
        self, 
        id:int, 
        data:CreatePatientRequest
    )->BaseResponse:
        try:
            if not id: return ForbiddenResponse()
            endpoint:str=os.getenv('PATIENT_REG')
            data=InternalCreatePatientRequest(**data.model_dump(), medical_staff_id=id)
            res=await self.post(endpoint=endpoint, data=data)
            json=res.json()
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            return CreatePatientResponse(
                code=json.get('code'),
                message=json.get('message'),
                id=json.get('id'),
            )
        except Exception as e:
            print(f'Patient service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            return ServerSideErrorResponse()
        
    async def update(
        self,
        id:int,
        data:UpdatePatientRequest
    )->BaseResponse:
        try:
            if not id: return ForbiddenResponse()
            endpoint:str=os.getenv('PATIENT_PUT')
            data=InternalUpdatePatientRequest(**data.model_dump(), medical_staff_id=id)
            res=await self.put(endpoint=endpoint, data=data)
            json=res.json()            
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            return UpdatePtaitenResponse(**json)
        except Exception as e:
            print(f'Patient service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            return ServerSideErrorResponse()
        
    async def deletePatient(
        self,
        id:int,
        data:DeletePatientRequest
    )->BaseResponse:
        try:
            if not id: return ForbiddenResponse()
            endpoint:str=os.getenv('PATIENT_DEL')
            data=InternalDeletePatientRequest(**data.model_dump(), medical_staff_id=id)
            res=await self.delete(endpoint=endpoint, data=data)
            json=res.json()            
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            return DeletePatientResponse(**json)
        except Exception as e:
            print(f'Patient service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            return ServerSideErrorResponse()