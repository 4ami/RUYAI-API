from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from model import PatientInformationModel
from view import (
    GetAllResponse,
    PatientInformation,
    Response500,
    BaseResponse,
    GetOneResponse
)

class PatientGET:
    @staticmethod
    async def all(
        medical_staff_id:int,
        page:int,
        session:AsyncSession
    )-> BaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')
            
            limit:int=10
            offset:int=(page-1) * limit
            
            query=select(PatientInformationModel).where(PatientInformationModel.medical_staff_id==medical_staff_id).limit(limit=limit).offset(offset=offset)
            result:Result=await session.execute(query)

            patients:list[PatientInformationModel]=result.scalars().all()
            ready:list[PatientInformation]=[
                PatientInformation(
                    id=p._id,
                    first_name=p.first_name,
                    middle_name=p.middle_name,
                    last_name=p.last_name,
                    birth_date=p.birth_date.strftime('%Y/%m/%d'),
                    gender=p.gender,
                    medical_history=p.medical_history
                )
                for p in patients
            ]
            
            return GetAllResponse(
                code=200,
                patients=ready
            )
        except Exception as e:
            print(f'Exception - {e}')
            return Response500()
    
    @staticmethod
    async def one(
        medical_staff_id:int,
        patient_id:int,
        session:AsyncSession
    ):
        try:
            if not session: raise Exception('Session is not initialized')

            query=select(PatientInformationModel).where(
                (PatientInformationModel._id == patient_id) & 
                (PatientInformationModel.medical_staff_id == medical_staff_id)
            )

            res:Result=await session.execute(query)
            info:PatientInformationModel=res.scalar_one_or_none()

            if info is None: return GetOneResponse(code=404, message='Patient is not found')

            patient:PatientInformation=PatientInformation(
                id=info._id,
                first_name=info.first_name,
                middle_name=info.middle_name,
                last_name=info.last_name,
                birth_date=info.birth_date.strftime('%Y/%m/%d'),
                gender=info.gender,
                medical_history=info.medical_history
            )
            return GetOneResponse(code=200, patient=patient)
        except Exception as e:
            print(f'Exception - {e}')
            return Response500()