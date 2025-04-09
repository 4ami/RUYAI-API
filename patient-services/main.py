from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

app:FastAPI=FastAPI(
    title='Patient Managment Services',
    summary='Service manages patients information',
)

from fastapi import Query
from core import GET_ENGINE
from sqlalchemy.ext.asyncio import AsyncSession

@app.get('/')
def ping(): return JSONResponse(content={'message': 'pong', 'health': 'Running', 'code': 200}, status_code=200)

from controller import PatientGET
from view import (
    BaseResponse,
    GetAllResponse
)
@app.get(
    path='/patients/{hospital_id}',
    status_code=200,
    description='Retrieve all hospital patients',
    response_model=GetAllResponse
)
async def get(
    hospital_id:int, 
    page:int=Query(1, ge=1, description='page number'), 
    session: AsyncSession | None = Depends(GET_ENGINE)
)-> BaseResponse:
    patients:BaseResponse=await PatientGET.all(hospital_id=hospital_id, page=page, session=session)
    
    if not isinstance(patients, GetAllResponse): 
        return JSONResponse(
            status_code=patients.code,
            content=patients.model_dump()
        )

    return patients