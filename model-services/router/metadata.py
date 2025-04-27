from fastapi import APIRouter, Depends
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
import asyncio

metadata_router:APIRouter=APIRouter(
    prefix='/metadata',
    tags=['Metadata']
)

from view import MetadtataResponse

from controller import DiagnoseReportController, FeedbackController, ImageSetController

@metadata_router.get(
    path='/staff/{sid}',
    response_model=MetadtataResponse,
    status_code=200
)
async def gether_metadata(
    sid:int,
    session:AsyncSession|None=Depends(GET_ENGINE)
):
    reports= await DiagnoseReportController.all_staff_reports_ids(sid=sid, session=session)
    reviewed= await DiagnoseReportController.all_staff_reviewd_reprots(sid=sid, session=session)
    recent_patients= await DiagnoseReportController.recently_diagnosed(sid=sid, session=session)

    # reports, reviewed, recent_patients = await asyncio.gather(reports_task, reviewed_task, recent_patients_task)
    
    uploads_task = ImageSetController.count_total_uploaded(reports=reports, session=session)
    pendings_task = DiagnoseReportController.count_pending(sid=sid, session=session)
    submissions_task = FeedbackController.total_submissions(reprots=reports, session=session)
    reviewed_reports_task = FeedbackController.total_reviewed_today(reviewed_reports=reviewed, session=session)
    recent_diagnosis_task = ImageSetController.last_daignosis(recents=recent_patients, session=session)


    uploads, pendings, submissions, reviewed_reports, recent_diagnosis = await asyncio.gather(uploads_task, pendings_task, submissions_task, reviewed_reports_task, recent_diagnosis_task)

    return MetadtataResponse(
        code=200,
        message="Metadata gathered successfully",
        total_uploads=uploads if uploads else 0,
        total_pending_reports=pendings if pendings else 0,
        total_submissions=submissions if submissions else 0,
        today_reviewed=reviewed_reports if reviewed_reports else 0,
        recent_diagnosis= recent_diagnosis if recent_diagnosis else []
    )
    
