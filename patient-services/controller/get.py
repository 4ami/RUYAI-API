from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from model import PatientInformationModel
from view import (
    GetAllResponse,
    PatientInformation,
    Response500,
    BaseResponse
)

class PatientGET:
    async def all(
        hospital_id:int,
        page:int,
        session:AsyncSession
    )-> BaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')
            
            limit:int=10
            offset:int=(page-1) * limit
            
            query=select(PatientInformationModel).where(PatientInformationModel.hospital_id==hospital_id).limit(limit=limit).offset(offset=offset)
            result:Result=await session.execute(query)

            patients:list[PatientInformationModel]=result.scalars().all()

            ready:list[PatientInformation]=[
                PatientInformation(
                    _id=p._id,
                    first_name=p.first_name,
                    middle_name=p.middle_name,
                    last_name=p.last_name,
                    birth_date=p.birth_date,
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