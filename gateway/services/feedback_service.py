from .base_service import BaseService
from utility import AVAILABLE_SERVICES

from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from dotenv import load_dotenv
import os
load_dotenv()

from views import (
    BaseResponse,
    AddFeedbackRequest,
    InternalAddFeedbackRequest,
    ServerSideErrorResponse,
    ForbiddenResponse
)

class FeedbackService(BaseService):
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
   
    async def add_feedback(
        self,
        sid:int,
        data:AddFeedbackRequest
    )->BaseResponse:
        try:
            if not sid: return ForbiddenResponse()
            endpoint:str=os.getenv('FEEDBACK_ADD')
            data=InternalAddFeedbackRequest(staff_id=sid, **data.model_dump())
            res=await self.post(endpoint=endpoint, data=data)
            json=res.json()
            if res.status_code == 422:
                from fastapi.exceptions import HTTPException
                raise HTTPException(status_code=res.status_code, detail=json['detail'])
            return BaseResponse(**json)
        except Exception as e:
            print(f'Feedback service exception:\n{e}')
            if isinstance(e, HTTPException):raise e
            raise HTTPException(
                status_code=ServerSideErrorResponse().code,
                detail=ServerSideErrorResponse().model_dump()
            )