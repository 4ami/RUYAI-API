from ..base import ResponseBaseModel
from pydantic import Field
from typing import Optional
from .report_metadata import ReportDiagnosisMetadata

class StaffReportsResponse(ResponseBaseModel):
    total_pages:Optional[int]=Field(
        default=None,
        title='Total Pages'
    )
    reports:Optional[list[ReportDiagnosisMetadata]]=Field(
        default=None,
        description='List of medical staff generated reports metadata for preview'
    )