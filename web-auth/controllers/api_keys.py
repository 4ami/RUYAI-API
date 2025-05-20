from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from utility import TokenHelper
import secrets
import time
import random

from sqlalchemy.future import select

from models import UserModel

from views import (
    ServerSideErrorResponse,
    GenerateApiKeyResponse
)

class ApiKeysController:
    @staticmethod
    async def generate(
        id:int,
        session: AsyncSession | None
    ):
        try:
            if session is None: raise Exception('Session is not initialized')

            stmt = select(UserModel).where(UserModel._id == id)
            res:Result = await session.execute(stmt)
            user:UserModel = res.scalar_one_or_none()

            if not user: return GenerateApiKeyResponse(code=403, message='Not allowed')

            if user.role != 2: return GenerateApiKeyResponse(code=403, message='Not allowed')


            key = f'sk_{secrets.token_hex(32)}'
            
            timestamps = int(time.time() * 1000)
            node = id & 0x3FF
            rand_seq = random.getrandbits(12)
            _id = ((timestamps & 0x1FFFFFFFFFF) << 22) | (node << 12) | rand_seq

            payload:dict = {
                '_id': _id,
                'key': key
            }

            api_key:str = TokenHelper.key(payload=payload)
            return GenerateApiKeyResponse(
                code=201,
                message='Api Key Generated Successfully, keep it safe.',
                token=api_key
            )
        except Exception as e:
            print(f'Api-Key controller:\n{e}')
            return ServerSideErrorResponse()

