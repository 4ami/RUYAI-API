from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services import FeedbackService
from views import BaseResponse, AddFeedbackRequest

feedback_router:APIRouter = APIRouter(
    prefix='/feedback-service',
    tags=['Feedback']
)

__SERVICE__:FeedbackService= FeedbackService()

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
    