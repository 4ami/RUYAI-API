from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from services import FeedbackService, ModelService
from views import BaseResponse, AddFeedbackRequest

feedback_router:APIRouter = APIRouter(
    prefix='/feedback-service',
    tags=['Feedback']
)

__SERVICE__:FeedbackService= FeedbackService()
__AI__:ModelService = ModelService()

feedback_router.dependencies=[Depends(__SERVICE__.check_service)]

@feedback_router.post(
    path='/new',
    status_code=201,
    response_model=BaseResponse
)
async def add_feedback(
    req:AddFeedbackRequest,
    sid:int=Depends(__SERVICE__.extractMID)
):
    res:BaseResponse=await __SERVICE__.add_feedback(sid=sid, data=req)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

from views import StaffReportsResponse
@feedback_router.get(
    path='/reports/pendings',
    status_code=200,
    response_model=StaffReportsResponse
)
async def get_pindings(
    sid:int=Depends(__AI__.extractMID),
    page:int=Query(default=1, description='reports page', ge=1)
)-> BaseResponse:
    res:BaseResponse = await __AI__.pending_reports(sid=sid, page=page)
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )
