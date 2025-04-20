from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from model import ImageSetModel, GlaucomaDiagnose
from fastapi import UploadFile
from utility import PathManager, ModelManager, CNN, Destination, ModelType
from sqlalchemy.future import select
import numpy as np
from view import (
    ResponseBaseModel, 
    Diagnosis200, 
    Diagnosis, 
    ServerSideErrorResponse, 
    ReportMetadata,
    DiagnoseMetadata,
    CompleteDiagnose,
    ImageMetadata,
    ImageInformation
)

__THRESHOLD__:float=0.5

class ImageSetController:
    @staticmethod
    async def add(
        report_id:int,
        octs:list[UploadFile],
        session: AsyncSession | None
    )-> ResponseBaseModel:
        try:
            if not session: raise Exception('Session is not initialized!')
            if not report_id: raise Exception('Report Id is None!')

            binary=ModelManager(architecture=CNN.FineTuned_EfficientNetV2B3_Binary)
            sevirty=ModelManager(architecture=CNN.FineTuned_Classification_V2B3)

            imgs:list[tuple[str, str]]=PathManager.store_uploaded(octs=octs)
            diagnosis:list[Diagnosis] = []
            
            for img in imgs:
                img_diagnose:ImageSetModel= ImageSetController._create_image(img=img, report_id=report_id)
                
                img_diagnose.glaucoma_confidence=float(
                    binary.classifiy(img=img[0], type_= ModelType.DETECTION)[0][0]
                )
                img_diagnose.glaucoma_diagnose = ImageSetController.__binary_class(pred=img_diagnose.glaucoma_confidence)
                print(f'Confidence: {img_diagnose.glaucoma_confidence}')
                grade = sevirty.classifiy(img=img[0], type_=ModelType.CLASSIFICATION)
                grade:int= np.argmax(grade, axis=1)[0]
                img_diagnose.severity= sevirty.map_severity(predection=grade)

                session.add(img_diagnose)
                await session.commit()
                diagnosis.append(ImageSetController.__fill_diagnose(data=img_diagnose, sent=img[1]))

            
            return Diagnosis200(report_id=report_id, diagnosis=diagnosis)
        except Exception as e:
            print(f'ImageSetController Exception:\n{e}')
            return ServerSideErrorResponse()
    
    @staticmethod
    def _create_image(img:tuple[str,str], report_id:int)->ImageSetModel:
        img_diagnose:ImageSetModel= ImageSetModel()
        img_diagnose.name= img[0].split('.')[0]
        img_diagnose.extension = img[1].split('.')[-1]
        img_diagnose.path= Destination.ROOT.value
        img_diagnose.report_id= report_id
        return img_diagnose
    
    @staticmethod
    def __binary_class(pred:float, threshold:float=__THRESHOLD__)->str:
        return GlaucomaDiagnose.POSITIVE.value if pred >= threshold else GlaucomaDiagnose.NEGATIVE.value
    
    @staticmethod
    def __fill_diagnose(data:ImageSetModel, sent:str, thrshold:float=__THRESHOLD__)->Diagnosis:
        return Diagnosis(
            image_sent=sent,
            stored_as=data.name,
            glaucoma=data.glaucoma_diagnose,
            glaucoma_propability=data.glaucoma_confidence,
            threshold_used=thrshold,
            severity=data.severity
        )
    
    @staticmethod
    async def getAll(
        rmd:ReportMetadata,
        session: AsyncSession | None
    )-> list[DiagnoseMetadata]|None:
        try:
            if not session: raise Exception('Session is not initialized!')
            
            stmt=select(ImageSetModel).where(
                (ImageSetModel.report_id == rmd.report_id)
            )

            res:Result=await session.execute(stmt)
            data:list[ImageSetModel]=res.scalars().all()
            if not data: return None

            return [
                DiagnoseMetadata(
                    id=i._id,
                    glaucoma_diagnose=i.glaucoma_diagnose,
                    severity=i.severity
                )
                for i in data
            ]
        except Exception as e:
            print(f'ImageSetController Exception:\n{e}')
            return None
    
    @staticmethod
    async def getFull(
        rmd:ReportMetadata,
        session: AsyncSession | None
    )-> list[CompleteDiagnose]|None:
        try:
            if not session: raise Exception('Session is not initialized!')
            
            stmt=select(ImageSetModel).where(
                (ImageSetModel.report_id == rmd.report_id)
            )

            res:Result=await session.execute(stmt)
            data:list[ImageSetModel]=res.scalars().all()
            if not data: return None

            return [
                CompleteDiagnose(
                    id=i._id,
                    glaucoma_diagnose=i.glaucoma_diagnose,
                    severity=i.severity,
                    glaucoma_confidence=i.glaucoma_confidence,
                    image=ImageMetadata(image=i.name.__str__(), ext=i.extension)
                )
                for i in data
            ]
        except Exception as e:
            print(f'ImageSetController Exception:\n{e}')
            return None
        
    @staticmethod
    async def get_image(
        image:str,
        session: AsyncSession | None
    )->ImageInformation | None:
        try:
            if not session: raise Exception('Session is not initialized!')
            split=image.split('.')
            name=split[0]
            ext=split[-1]
            if not name: raise Exception('Invalid name')

            stmt=select(ImageSetModel).where(
                (ImageSetModel.name == name) &
                (ImageSetModel.extension==ext)
            )

            res:Result=await session.execute(stmt)
            data:ImageSetModel=res.scalar_one_or_none()
            if not data: return None

            return ImageInformation(
                image=name,
                ext=ext,
                report_id= data.report_id,
                path=data.path
            )
        except Exception as e:
            print(f'ImageSetController Exception:\n{e}')
            return None