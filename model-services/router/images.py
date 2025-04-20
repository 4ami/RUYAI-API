from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core import GET_ENGINE
from view import ResponseBaseModel, ImageInformation
from controller import ImageSetController, DiagnoseReportController
from utility import PathManager

images_router:APIRouter = APIRouter(
    prefix='/images',
    tags=['Diagnosed Images']
)

@images_router.get(
    path='staff/{sid}/image/{image}',
    status_code=200,
)
async def get_image(
    sid:int,
    image:str,
    session: AsyncSession | None = Depends(GET_ENGINE)
):
    info:ImageInformation=await ImageSetController.get_image(image=image, session=session)
    if not info:
        nf=ResponseBaseModel(code=404, message='Not found / invalid image name')
        return JSONResponse(status_code=nf.code,content=nf.model_dump())
    
    isAllowed:bool=await DiagnoseReportController.can_get(rid=info.report_id, sid=sid, session=session)

    if not isAllowed:
        na=ResponseBaseModel(code=403, message='Forbidden')
        return JSONResponse(status_code=na.code, content=na.model_dump())
    
    path:str = PathManager.read_image(name=info.image, ext=info.ext, path=info.path)

    if not path:
        nf=ResponseBaseModel(code=404, message='Not found')
        return JSONResponse(status_code=nf.code,content=nf.model_dump())

    return FileResponse(path=path, status_code=200, media_type=f'image/{info.ext}')