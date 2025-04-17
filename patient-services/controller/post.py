from sqlalchemy.ext.asyncio import AsyncSession
from model import PatientInformationModel
from view import CreatePatientRequest, Response500, BaseResponse, CreatePatientResponse
from utility import HTTPClient, HttpMethods
from datetime import datetime


class PatientPOST:
    @staticmethod
    async def create(
        data:CreatePatientRequest,
        session: AsyncSession | None
    )-> BaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')
            # is_exists = HTTPClient.request(method=HttpMethods.GET)

            new_patient:PatientInformationModel = PatientInformationModel(
                first_name=data.first_name,
                middle_name=data.middle_name,
                last_name=data.last_name,
                birth_date=datetime.strptime(data.birth_date, "%Y/%m/%d"),
                gender=data.gender.upper(),
                medical_history=data.medical_history,
                medical_staff_id=data.medical_staff_id
            )

            session.add(new_patient)
            await session.commit()
            await session.refresh(new_patient)
            
            return CreatePatientResponse(
                code=201,
                id=new_patient._id 
            )
        except Exception as e:
            print(f'Exception: {e}')
            return Response500()
        finally:
            await session.close()