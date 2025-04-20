from fastapi import APIRouter, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core import GET_ENGINE
from view import ResponseBaseModel
from controller import ImageSetController, DiagnoseReportController

reports:APIRouter = APIRouter(
    prefix='/reports',
    tags=['Reports']
)

from view import StaffReportsResponse, ReportMetadata, ReportDiagnosisMetadata, DiagnoseMetadata
@reports.get(
    path='/{id}',
    description='All Staff\'s reports',
    response_model=StaffReportsResponse,
    status_code=200
)
async def getAll(
    id:int,
    page:int=Query(1, title='Page number', description='Returns reports in that page' ,ge=1),
    session:AsyncSession|None=Depends(GET_ENGINE)
)->ResponseBaseModel:
    rm:list[ReportMetadata] = await DiagnoseReportController.getAll(id=id, page=page, session=session)
    nfr=StaffReportsResponse(code=404, message='No reports found')
    if not rm:
        return JSONResponse(status_code=nfr.code, content=nfr.model_dump(exclude_none=True))
    
    rdm:list[ReportDiagnosisMetadata]= []

    for r in rm:
        dm:list[DiagnoseMetadata] = await ImageSetController.getAll(rmd=r, session=session)
        if not dm:
            return JSONResponse(status_code=nfr.code, content=nfr.model_dump(exclude_none=True))
        rdm.append(ReportDiagnosisMetadata(**r.model_dump(), diagnosis=dm))
    
    return StaffReportsResponse(code=200, message='Found Reports successfully', reports=rdm)


from view import CompleteDiagnose, FullReportResponse, FullReportData
@reports.get(
    path='/{rid}/staff/{sid}/patient/{pid}',
    status_code=200,
    response_model=FullReportResponse
)
async def getOne(
    rid:int,
    sid:int,
    pid:int,
    session:AsyncSession|None=Depends(GET_ENGINE)
)->ResponseBaseModel:
    nfr:ResponseBaseModel= ResponseBaseModel(code=404, message='No Report Fount')
    rmd:ReportMetadata = await DiagnoseReportController.getOne(rid=rid, sid=sid, pid=pid, session=session)

    if not rmd:
        return JSONResponse(status_code=nfr.code, content=nfr.model_dump(exclude_none=True))
    
    cd:list[CompleteDiagnose]=await ImageSetController.getFull(rmd=rmd, session=session)

    if not cd:
        return JSONResponse(status_code=nfr.code, content=nfr.model_dump(exclude_none=True))
    

    fd:FullReportData = FullReportData(
        **rmd.model_dump(),
        diagnose=cd
    )
    return FullReportResponse(code=200, message='Report Found', report=fd)