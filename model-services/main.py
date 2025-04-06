from fastapi import FastAPI
from fastapi.responses import JSONResponse

app:FastAPI = FastAPI(
    title='RuyAI Diagnosis Services',
    summary='Diagnose Patients\' OCT To Predict and Grade Their Glaucoma Signs and Severity'
)


@app.get('/ping')
def ping(): return JSONResponse(status_code=200, content={'message': 'pong', 'health': 'Running', 'code': 200})

from router import diagnosis_router
app.include_router(router=diagnosis_router)