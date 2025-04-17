from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from model import PatientInformationModel

from view import BaseResponse, DeletePatientRequest, DeleteResponse


class DeletePatientController:
    @staticmethod
    async def delete(
        data:DeletePatientRequest,
        session:AsyncSession|None
    )->BaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')

            stmt = select(PatientInformationModel).where(
                (data.id == PatientInformationModel._id) &
                (data.medical_staff_id == PatientInformationModel.medical_staff_id)
            )

            res:Result= await session.execute(stmt)

            patient:PatientInformationModel = res.scalar_one_or_none()

            if not patient: return DeleteResponse(code=404, message='Patient is not exist')

            await session.delete(patient)
            await session.commit()
            return DeleteResponse(code=200, message='Patient has been deleted')
        except Exception as e:
            print(f'Exception: ${e}')
        finally:
            if session: await session.close()