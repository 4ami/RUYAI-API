from .base_service import BaseService
from utility import AVAILABLE_SERVICES

from fastapi import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from dotenv import load_dotenv
import os
load_dotenv()

from views import (
    BaseResponse,
    ServerSideErrorResponse,
    ForbiddenResponse,
    DiagnoseRequest,
    InternalDiagnoseRequest,
    DiagnoseResponse,
    StaffReportsResponse,
    ModelFullReport,
    RawDashboardDataResponse
)

class ModelService(BaseService):
    def __init__(self):
        super().__init__(service=AVAILABLE_SERVICES.AI)
    
    async def check_service(self)->BaseResponse:
        try:
            unavailable_service:BaseResponse = BaseResponse(
                code=503,
                message='Model service is currently unavailable'
            )
            res=await self.get(endpoint='/ping')
            
            if res.status_code != 200:
                raise HTTPException(
                    status_code=unavailable_service.code,
                    detail=unavailable_service.model_dump()
                )
        except Exception as e:
            print(f'Model service exception:\n{e}')
            if e is HTTPException: raise e
            raise HTTPException(
                    status_code=ServerSideErrorResponse().code,
                    detail=ServerSideErrorResponse().model_dump()
                )
    

    async def extractMID(self, req:Request):
        if not hasattr(req.state, 'id'):
            raise HTTPException(
                status_code=ForbiddenResponse().code,
                detail=ForbiddenResponse().model_dump()
            )
        return req.state.id


    async def diagnose(
        self,
        data:DiagnoseRequest,
        sid:int,
        octs:list[UploadFile]
    ):
        try:
            if not sid: return ForbiddenResponse()
            oct_multipart:list[tuple[str, UploadFile]]=[]
            for oct in octs:
                oct_multipart.append(("octs", oct))
            data= InternalDiagnoseRequest(**data.model_dump(), staff_id=sid)
            endpoint:str=os.getenv('MODEL_DIAG')
            res=await self.post_multipart(
                endpoint=endpoint,
                fields=data.model_dump(),
                files=oct_multipart
            )
            json=res.json()
            if res.status_code == 422 or res.status_code==400:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            return DiagnoseResponse(**json)
        except Exception as e:
            print(f'Model service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump()
            )
    

    async def get_reports(
        self,
        sid:int,
        page:int
    ):
        try:
            if not sid: return ForbiddenResponse()
            endpoint:str=os.getenv('MODEL_REPORTS').format(sid=sid)
            res=await self.get(endpoint=endpoint, params={'page': page})
            json=res.json()
            
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
         
            return StaffReportsResponse(**json)
        except Exception as e:
            print(f'Model service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump()
            )
    

    async def get_image(
        self,
        sid:int,
        image:str,
    ):
        try:
            if not sid: return ForbiddenResponse()
            endpoint:str=os.getenv('MODEL_GET_IMAGE').format(sid=sid, image=image)
            res=await self.get(endpoint=endpoint)

            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            
            content_type:str = res.headers.get('content-type', "")
            if "application/json" in content_type:
                json=res.json()
                return BaseResponse(**json)

            if "image" in content_type:
                return StreamingResponse(
                    res.aiter_bytes(),
                    media_type=content_type
                )            
        except Exception as e:
            print(f'Model service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump()
            )
        
    async def report(
        self,
        rid:int,
        sid:int,
        pid:int
    ):
        try:
            if not sid: return ForbiddenResponse()
            endpoint:str=os.getenv('MODEL_PATIENT_REP').format(rid=rid, sid=sid, pid=pid)
            res=await self.get(endpoint=endpoint)
            json=res.json()
            
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])

            if not json.get('report'):
                return None

            return ModelFullReport(**(json.get('report')))
        except Exception as e:
            print(f'Model service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump()
            )
        
    async def dashboard_data(
        self,       
        sid:int,
    ):
        try:
            if not sid: return ForbiddenResponse()
            endpoint:str=os.getenv('METADATA_DASHBOARD').format(id=sid)
            res= await self.get(endpoint=endpoint)
            json= res.json()

            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            
            return RawDashboardDataResponse(**json)
        except Exception as e:
            print(f'Model service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump()
            )