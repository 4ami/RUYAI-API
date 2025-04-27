from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from .diagnose_report_controller import DiagnoseReportController
from view import AddFeedbackRequest
from model import FeedbackModel
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import date

class FeedbackController:

    @staticmethod
    async def add_feedback(
        data:AddFeedbackRequest,
        session: AsyncSession | None
    )->tuple[bool, str|None]:
        try:
            if not session: raise Exception('session is not initiallized!')

            async with session.begin():
                isUpdated = await DiagnoseReportController.update_approval_status(
                    approval_status=data.approval_status,
                    report_id=data.report_id,
                    staff=data.staff_id,
                    session=session
                )

                if not isUpdated[0]: raise Exception(isUpdated[1])

                stmt = select(FeedbackModel).where(FeedbackModel.report == data.report_id)
                res:Result= await session.execute(stmt)

                isExist= res.scalars().all()
                if isExist: raise Exception('Feedback is already submitted')

                newFeedback=FeedbackModel()
                newFeedback.comment = data.comment
                newFeedback.rate = data.rate
                newFeedback.report = data.report_id

                session.add(newFeedback)
            return True, None
        except Exception as e:
            print(f'FeedbackController exception:\n{e}')
            return False, e.__str__()
        finally:
            if session: await session.close()


    @staticmethod
    async def total_submissions(
        reprots:list[int],
        session: AsyncSession | None
    )->int|None:
        try:
            if not session: raise Exception('session is not initiallized!')
            stmt=select(func.count()).where(FeedbackModel.report.in_(reprots))
            res:Result=await session.execute(stmt)
            subs:int = res.scalar_one_or_none()
            if not subs: subs = 0
            return subs
        except Exception as e:
            print(f'FeedbackController exception:\n{e}')
            return None
        
    @staticmethod 
    async def total_reviewed_today(
        reviewed_reports:list[int],
        session: AsyncSession | None
    )->int | None:
        try:
            if not session: raise Exception('session is not initiallized!')
            
            stmt=select(func.count()).where(
                (FeedbackModel.report.in_(reviewed_reports)) &
                (FeedbackModel.submitted_at==date.today())
            )
            res:Result=await session.execute(stmt)
            total:int|None = res.scalar_one_or_none()
            if not total: total = 0
            return total
        except Exception as e:
            print(f'FeedbackController exception:\n{e}')
            return None