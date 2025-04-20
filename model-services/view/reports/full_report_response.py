from ..base import ResponseBaseModel
from pydantic import Field
from typing import Optional
from .report_metadata import FullReportData

class FullReportResponse(ResponseBaseModel):
    report:Optional[FullReportData]