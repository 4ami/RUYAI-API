from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services import ModelService, PatientService, AuthService

metadata_router:APIRouter = APIRouter(
    prefix='/metadata-service',
    tags=['Metadata']
)

__MODEL__:ModelService = ModelService()
__PATIENT__:PatientService = PatientService()
__AUTH__:AuthService= AuthService()

metadata_router.dependencies=[Depends(__AUTH__.CheckService)]

from views import AvailableRoles
@metadata_router.get(
    path='/roles',
    response_model=AvailableRoles,
    status_code=200
)
async def roles():
    res= await __AUTH__.get_roles()
    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )

metadata_router.dependencies=[Depends(__MODEL__.check_service)]


from views import DashboardDataResponseFull, RawDashboardDataResponse, RecentPatientDiagnoseFull, GetOnePatientResponse

@metadata_router.get(
    path='/dashboard/data',
    response_model=DashboardDataResponseFull,
    status_code=200
)
async def get_dashboard(
    sid:int = Depends(__MODEL__.extractMID)
):
    raw=await __MODEL__.dashboard_data(sid=sid)
    if not isinstance(raw, RawDashboardDataResponse):
        return JSONResponse(
            status_code=raw.code,
            content=raw.model_dump(exclude_none=True),
        )
    
    rd:list[RecentPatientDiagnoseFull]=[]
    for r in raw.recent_diagnosis:
        print('ENTERED')
        p=await __PATIENT__.getOne(mid=sid, pid=r.patient_id)
        if not isinstance(p, GetOnePatientResponse): continue
        print(p.model_dump())
        rd.append(
            RecentPatientDiagnoseFull(report_id=r.report_id, patient_info=p.patient, glaucoma=r.glaucoma, severity=r.severity)
        )
    
    res:DashboardDataResponseFull=DashboardDataResponseFull(
        code=200,
        message=raw.message,
        recent_diagnosis=rd,
        total_uploads=raw.total_uploads,
        total_pending_reports=raw.total_pending_reports,
        today_reviewed=raw.today_reviewed,
        total_submissions=raw.total_submissions,
    )

    return JSONResponse(
        status_code=res.code,
        content=res.model_dump(exclude_none=True)
    )