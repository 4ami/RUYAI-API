from sqlalchemy.engine import Result
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from utility import HashHelper, TokenHelper
from models import UserModel


from views import (
    RegisterResponseBase, 
    Register201, 
    Register400, 
    Register500, 
    RegisterRequest,
    #--Login Views--#
    LoginResponseBase,
    Login200,
    Login404,
    Login500,
    LoginRequest
)


class UserController:
    @staticmethod
    async def register(
        user: RegisterRequest,
        session:AsyncSession | None,
    )->RegisterResponseBase:
        try:
            # session is not resolved correctly
            if session is None: raise Exception()

            _select=select(UserModel.email).where(UserModel.email==user.email)
            _select_res:Result= await session.execute(_select)
            _usr:UserModel | None= _select_res.scalar_one_or_none()
            
            # account is already exist
            if _usr: return Register400()

            hashed, salt=HashHelper.hash(user.password)
            to_add:UserModel= UserModel(
                full_name=user.full_name,
                email=user.email,
                password=hashed,
                salt=salt
            )

            session.add(to_add)
            await session.commit()
            await session.refresh(to_add)

            return Register201()
        except Exception as e:
            print(e)
            return Register500()
        
    @staticmethod
    async def login(
        credentials:LoginRequest,
        session:AsyncSession | None
    )->LoginResponseBase:
        try:
            # session is not resolved correctly
            if session is None: raise Exception()

            # find user by email
            _select=select(UserModel).where(UserModel.email==credentials.email)
            _res:Result= await session.execute(_select)
            _usr:UserModel | None = _res.scalar_one_or_none()

            # user is not exist
            if _usr is None: return Login404()
            

            # compare credentials
            if not HashHelper.compare(
                hashed=_usr.password,
                salt=_usr.salt,
                password=credentials.password
            ): return Login404()

            # generate token pairs
            _1, _2 = TokenHelper.user_pair_tokens(
                payload={
                    '_id': _usr._id,
                    'full_name': _usr.full_name,
                    'role': _usr.role
                }
            )
            return Login200(
                token=_1,
                ref_toke=_2
            )
        except Exception as e:
            print(e)
            return Login500()