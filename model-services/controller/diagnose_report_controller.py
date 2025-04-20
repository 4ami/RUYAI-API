from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from view import DiagnoseRequest, ReportMetadata
from model import DiagnoseReportModel
from sqlalchemy.future import select

class DiagnoseReportController:
    @staticmethod
    async def create_report(
        data:DiagnoseRequest,
        session:AsyncSession|None
    )->int|None:
        try:
            if not session: raise Exception('Session is not initialized!')
            report:DiagnoseReportModel= DiagnoseReportModel()
            report.request_by=data.staff_id
            report.belongs_to=data.patient_id
            session.add(report)
            await session.commit()
            await session.refresh(report)
            return report._id
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        finally:
            if session: await session.close()

    @staticmethod
    async def getAll(
        id:int,
        page:int,
        session:AsyncSession|None
    )->list[ReportMetadata] | None:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not id: raise Exception('Missing ID')
            
            limit:int=10
            offset:int=(page-1)*limit
            
            stmt=select(DiagnoseReportModel).where(
                DiagnoseReportModel.request_by == id
            ).limit(limit=limit).offset(offset=offset)
            

            res:Result=await session.execute(stmt)
            data:list[DiagnoseReportModel] = res.scalars().all()
            if not data: return None

            return [
                ReportMetadata(
                    report_id=r._id, 
                    patient_id=r.belongs_to,
                    approval_status=r.approval_status,
                    created_at=r.created_at
                )
                for r in data
            ]
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        
    @staticmethod
    async def getOne(
        rid:int,
        sid:int,
        pid:int,
        session:AsyncSession|None
    )->ReportMetadata|None:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not rid or not sid or not pid: raise Exception('Missing ID')
            
            stmt=select(DiagnoseReportModel).where(
                (DiagnoseReportModel._id == rid) &
                (DiagnoseReportModel.request_by == sid) &
                (DiagnoseReportModel.belongs_to == pid) 
            )

            res:Result=await session.execute(stmt)
            data:DiagnoseReportModel=res.scalar_one_or_none()
            if not data: return None

            return ReportMetadata(
                report_id=data._id, 
                patient_id=data.belongs_to,
                approval_status=data.approval_status,
                created_at=data.created_at
            )
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        
    @staticmethod
    async def can_get(
        rid:int,
        sid:int,
        session:AsyncSession|None
    )->bool:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not rid or not sid: raise Exception('Missing ID')

            stmt=select(DiagnoseReportModel).where(
                (DiagnoseReportModel._id == rid) &
                (DiagnoseReportModel.request_by == sid)
            )

            res:Result=await session.execute(stmt)
            data:DiagnoseReportModel=res.scalar_one_or_none()
            if not data: return False

            return True
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return False