from ..base_response import BaseResponse
from pydantic import Field
from typing import Optional
from .recent_diagnose_data import RecentPatientDiagnose, RecentPatientDiagnoseFull

class RawDashboardDataResponse(BaseResponse):
    total_uploads:Optional[int]=Field(
        default=0,
        title='Total OCT Uploads'
    )
    total_pending_reports:Optional[int]=Field(
        default=0,
        title='Total Pending Reports'
    )
    today_reviewed:Optional[int]=Field(
        default=0,
        title='Total Reports Reviewed Today'
    )
    total_submissions:Optional[int]=Field(
        default=0,
        title='Total Reports Feedbacks submitted'
    )
    recent_diagnosis:Optional[list[RecentPatientDiagnose]]=Field(
        default=[],
        title='Recent Diagnosis'
    )


class DashboardDataResponseFull(RawDashboardDataResponse):
    recent_diagnosis:Optional[list[RecentPatientDiagnoseFull]]=Field(
        default=[],
        title='Recent Diagnosis'
    )