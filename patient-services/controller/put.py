from sqlalchemy.ext.asyncio import AsyncSession
from model import PatientInformationModel
from view import UpdatePatientInfoRequest, BaseResponse, Response500, UpdatedPatientInfoResponse
from sqlalchemy.future import select
from sqlalchemy.engine import Result
from datetime import datetime

class PatientInfoPUT:
    @staticmethod
    async def update(
        data:UpdatePatientInfoRequest,
        session:AsyncSession|None
    )->BaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')

            qury=select(PatientInformationModel).where(
                (PatientInformationModel._id == data.id) &
                (PatientInformationModel.medical_staff_id == data.medical_staff_id)
            )

            res:Result= await session.execute(qury)
            
            old:PatientInformationModel=res.scalar_one_or_none()

            if not old:
                return UpdatedPatientInfoResponse(code=404, message='Patient\'s information failed to updated.')
            
            old.first_name= data.first_name if data.first_name else old.first_name
            old.middle_name= data.middle_name if data.middle_name else old.middle_name
            old.last_name= data.last_name if data.last_name else old.last_name
            old.birth_date= datetime.strptime(data.birth_date, "%Y/%m/%d") if data.birth_date else old.birth_date
            old.gender= data.gender.upper() if data.gender else old.gender
            old.medical_history= data.medical_history if data.medical_history else old.medical_history

            await session.commit()
            await session.refresh(old)

            return UpdatedPatientInfoResponse(
                code=200,
                first_name=old.first_name,
                middle_name= old.middle_name,
                last_name=old.last_name,
                birth_date=old.birth_date.strftime("%Y/%m/%d"),
                gender=old.gender,
                medical_history=old.medical_history if old.medical_history else dict()
            )
        except Exception as e:
            print(f'Exception: {e}')
            return Response500()
        finally:
            await session.close()