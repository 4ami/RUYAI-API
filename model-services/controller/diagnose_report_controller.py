from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from view import DiagnoseRequest, ReportMetadata
from model import DiagnoseReportModel
from sqlalchemy.future import select
from sqlalchemy import func, distinct
from datetime import date

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
    )->tuple[list[ReportMetadata] | None, int | None]:
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
            if not data: return None, None

            count=select(func.count()).select_from(DiagnoseReportModel).where(
                DiagnoseReportModel.request_by == id
            )

            count_res:Result=await session.execute(count)
            total= count_res.scalar_one_or_none()
            if not total: total = 0
            total= max((total + limit-1)//limit, 1)

            return [
                ReportMetadata(
                    report_id=r._id, 
                    patient_id=r.belongs_to,
                    approval_status=r.approval_status,
                    created_at=r.created_at
                )
                for r in data
            ], total
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None, None
        
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
        
    @staticmethod
    async def update_approval_status(
        approval_status:str,
        report_id:int,
        staff:int,
        session: AsyncSession | None        
    )->tuple[bool, str|None]:
        try:
            if not session: raise Exception('Session is not initialized!')
            
            stmt=select(DiagnoseReportModel).where(
                (DiagnoseReportModel._id == report_id) &
                (DiagnoseReportModel.request_by == staff)
            )
            res:Result=await session.execute(stmt)
            report:DiagnoseReportModel=res.scalar_one_or_none()
            if not report: raise Exception('Report not found')

            report.approval_status=approval_status
            return True, None
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return False, e.__str__()
    
    @staticmethod
    async def all_staff_reports_ids(
        sid:int,
        session: AsyncSession | None   
    )->list[int] | None:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not sid : raise Exception('Missing ID')

            stmt=select(DiagnoseReportModel._id).where(DiagnoseReportModel.request_by==sid)
            res:Result = await session.execute(stmt)

            data:list[int]=res.scalars().all()
            if not data: return None
            return data
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        
    @staticmethod
    async def count_pending(
        sid:int,
        session: AsyncSession | None 
    )->  int | None:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not sid : raise Exception('Missing ID')

            stmt=select(func.count()).where(
                (DiagnoseReportModel.request_by==sid) &
                (DiagnoseReportModel.approval_status=="PENDING")
            )

            res:Result=await session.execute(stmt)
            pendings:int=res.scalar_one_or_none()
            if not pendings: pendings=0

            return pendings
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        
    @staticmethod
    async def all_staff_reviewd_reprots(
        sid:int,
        session: AsyncSession | None   
    )->list[int] | None:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not sid : raise Exception('Missing ID')

            stmt=select(DiagnoseReportModel._id).where(
                (DiagnoseReportModel.request_by == sid)&
                (DiagnoseReportModel.approval_status.in_(["APPROVED", "REJECTED"]))
            )
            res:Result= await session.execute(stmt)
            reviewed:list[int]= res.scalars().all()
            print(reviewed)
            if not reviewed: return None
            return reviewed
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        
    @staticmethod
    async def recently_diagnosed(
        sid:int,
        session: AsyncSession | None   
    )->list[tuple[int, int]]| None:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not sid : raise Exception('Missing ID')

            stmt=select(
                distinct(DiagnoseReportModel.belongs_to),
                DiagnoseReportModel._id
            ).where(
                (DiagnoseReportModel.request_by == sid)&
                (DiagnoseReportModel.created_at == date.today())
            ).order_by(
                DiagnoseReportModel._id.desc()
            ).limit(2)

            res:Result = await session.execute(stmt)
            recent:list[tuple[int, int]] = res.all()
            if not recent: return None
            return recent
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None
        
    @staticmethod
    async def get_pendings(
        id:int,
        page:int,
        session:AsyncSession | None 
    )->tuple[list[ReportMetadata] | None, int | None]:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not id: raise Exception('Missing ID')
            
            limit:int=10
            offset:int=(page-1)*limit

            stmt=select(DiagnoseReportModel).where(
                (DiagnoseReportModel.request_by == id) &
                (DiagnoseReportModel.approval_status == "PENDING")
            ).limit(limit=limit).offset(offset=offset)

            res:Result = await session.execute(stmt)
            data:list[DiagnoseReportModel] = res.scalars().all()

            count=select(func.count()).select_from(DiagnoseReportModel).where(
                (DiagnoseReportModel.request_by == id) &
                (DiagnoseReportModel.approval_status == "PENDING")
            )

            count_res:Result=await session.execute(count)
            total= count_res.scalar_one_or_none()
            if not total: total = 0
            total= max((total + limit-1)//limit, 1)

            return [
                ReportMetadata(
                    report_id= r._id,
                    patient_id= r.belongs_to,
                    approval_status= r.approval_status,
                    created_at=r.created_at
                )
                for r in data
            ], total
        except Exception as e:
            print(f'DiagnoseReportController Exception:\n{e}')
            return None, None