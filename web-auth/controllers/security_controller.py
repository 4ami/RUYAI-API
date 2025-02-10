from sqlalchemy.ext.asyncio  import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy.future import select

from models import UserModel

from views import (
    LockRequest,
    LockBaseResponse,
    Lock200,
    Lock400,
    Lock404,
    Lock409,
    Lock500,
    #--Unlock--#
    UnLockRequest,
    UnLockBaseResponse,
    UnLock200,
    UnLock400,
    UnLock404,
    UnLock409,
    UnLock500
)

class SecurityController:
    @staticmethod
    async def lock_account(
        inf:LockRequest,
        session:AsyncSession | None
    ) -> LockBaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')
            # if email is not provided assign account_id else email is assignd
            _identifier= inf.account_id if not inf.email else inf.email
            
            # if both are missing return bad request
            if not _identifier: return Lock400()
            
            #make the right query
            _select=select(UserModel).where(UserModel.email == _identifier if inf.email else UserModel._id == _identifier)
            _res:Result= await session.execute(_select)
            _usr:UserModel= _res.scalar_one_or_none()
            
            # User is not exist
            if _usr is None: return Lock404()

            # User account already locked
            if _usr.locked: return Lock409()

            _usr.locked=True
            await session.commit()
            return Lock200()
        except Exception as e:
            print(e)
            return Lock500()
    
    @staticmethod
    async def unlock(
        inf:UnLockRequest,
        session:AsyncSession | None
    )->UnLockBaseResponse:
        try:
            if not session: raise Exception('Session is not initialized')
            # if email is not provided assign account_id else email is assignd
            _identifier= inf.account_id if not inf.email else inf.email
            
            # if both are missing return bad request
            if not _identifier: return UnLock400()

            _select=select(UserModel).where(UserModel.email == _identifier if inf.email else UserModel._id == _identifier)
            _res:Result= await session.execute(_select)
            _usr:UserModel= _res.scalar_one_or_none()

            # User is not exist
            if _usr is None: return UnLock404()


            # User account already unlocked
            if not _usr.locked: return UnLock409()

            _usr.locked=False
            _usr.locked_at=None
            await session.commit()
            return UnLock200()
        except Exception as e:
            print(e)
            return UnLock500()
        