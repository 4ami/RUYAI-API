from fastapi import APIRouter, Depends
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

feedback_router:APIRouter=APIRouter(
    prefix='/feedback',
    tags=['Feedback']
)

from view import AddFeedbackRequest, ResponseBaseModel
from controller import FeedbackController

@feedback_router.post(
    path='/new',
    status_code=201,
    response_model=ResponseBaseModel
)
async def add_feedback(
    req:AddFeedbackRequest,
    session:AsyncSession|None=Depends(GET_ENGINE)
)->ResponseBaseModel:
    isAdded:bool = await FeedbackController.add_feedback(data=req, session=session)
    res:ResponseBaseModel = ResponseBaseModel(code=201, message='Your Feedback Submitted Successfully')
    if not isAdded[0]:
        res.code = 400
        res.message = isAdded[1]
        return JSONResponse(
            status_code=res.code,
            content=res.model_dump(exclude_none=True)
        )
    return res