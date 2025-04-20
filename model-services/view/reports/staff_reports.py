from ..base import ResponseBaseModel
from pydantic import Field
from typing import Optional
from .report_metadata import ReportDiagnosisMetadata

class StaffReportsResponse(ResponseBaseModel):
    reports:Optional[list[ReportDiagnosisMetadata]]=Field(
        default=None,
        description='List of medical staff generated reports metadata for preview'
    )