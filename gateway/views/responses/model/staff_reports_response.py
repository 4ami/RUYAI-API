from ..base_response import BaseResponse
from .report_metadata import ReportMetadata
from typing import Optional
from pydantic import Field

class StaffReportsResponse(BaseResponse):
    total_pages:Optional[int]=Field(
        default=None,
        title='Total Pages'
    )
    reports:Optional[list[ReportMetadata]]=Field(
        default=None,
        title='Reports Metadata'
    )