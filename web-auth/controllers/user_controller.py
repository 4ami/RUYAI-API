from sqlalchemy.engine import Result
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from .role_controller import RoleController

from utility import HashHelper, TokenHelper, MailUtil
from models import UserModel, ForgetPasswordTokenModel
import secrets
from datetime import timedelta, datetime
from pytz import timezone

from views import (
    RegisterResponseBase, 
    ServerSideErrorResponse,
    Register201, 
    Register400, 
    Register500, 
    RegisterRequest,
    #--Login Views--#
    LoginResponseBase,
    Login200,
    Login403,
    Login404,
    Login500,
    LoginRequest,
    #--User/Admin--#
    AdminUpdateUserRequest,
    AdminUpdateUserResponse,
    PendingAccountsResponse,
    PendingAccountsInformation,
    #--ForgetPassword--#
    ForgetPasswordRequest,
    ForgetPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    UserAccountsResponse
)


class UserController:
    @staticmethod
    async def register(
        user: RegisterRequest,
        session:AsyncSession | None,
    )->RegisterResponseBase:
        try:
            # session is not resolved correctly
            if session is None: raise Exception('Session is not Initialized')

            _select=select(UserModel.email).where(UserModel.email==user.email)
            _select_res:Result= await session.execute(_select)
            _usr:UserModel | None= _select_res.scalar_one_or_none()
            
            # account is already exist
            if _usr: return Register400()

            # check role is allowed
            isValid = await RoleController.check_valid_role(role=user.role, session=session)

            if not isValid: return Register400(message='Attempting to register invalid role')


            hashed, salt=HashHelper.hash(user.password)
            to_add:UserModel= UserModel(
                full_name=user.full_name,
                email=user.email,
                password=hashed,
                salt=salt,
                role=user.role
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
            if session is None: raise Exception('Session is not Initialized')

            # find user by email
            _select=select(UserModel).where(UserModel.email==credentials.email)
            _res:Result= await session.execute(_select)
            _usr:UserModel | None = _res.scalar_one_or_none()

            # user is not exist
            if _usr is None: return Login404()
            
            # if account is locked return early
            if _usr.locked: return Login403()

            # if user account still pending
            if _usr.account_status == "PENDING": return Login403(message='Accound Still Pending')
            
            # if accound is disabled
            if _usr.account_status == "DISABLED": return Login403(message='Accound is DISABLED. Contact with Admin')

            # compare credentials
            if not HashHelper.compare(
                hashed=_usr.password,
                salt=_usr.salt,
                password=credentials.password
            ): return Login404()


            #get role name
            # role = await RoleController.get_role_name(role=_usr.role, session=session)
            # if not role: role = "INVALID ROLE"

            # generate token pairs
            _1, _2 = TokenHelper.user_pair_tokens(
                payload={
                    '_id': _usr._id,
                    'full_name': _usr.full_name,
                    'email': _usr.email,
                    'role': _usr.role,
                }
            )
            return Login200(
                token=_1,
                ref_token=_2
            )
        except Exception as e:
            print(e)
            return Login500()
        
    @staticmethod
    async def edit_user_admin(
        data:AdminUpdateUserRequest,
        session:AsyncSession | None
    ):
        try:
            if session is None: raise Exception('Session is not Initialized')
            
            stmt=select(UserModel).where(
                UserModel._id == data.user_id
            )
            res:Result=await session.execute(stmt)
            user:UserModel = res.scalar_one_or_none()

            if not user: return AdminUpdateUserResponse(code=400, message='Invalid request')

            is_admin = await RoleController.is_admin(role=user.role, session=session)

            if is_admin: return AdminUpdateUserResponse(code=403, message='Updating Admin Data is Not Allowed')
            
            if data.user_information.role:
                new_role_is_admin = await RoleController.is_admin(role=data.user_information.role, session=session)
                if new_role_is_admin: return AdminUpdateUserResponse(code=403, message='Escalating User Role is Not Allowed.')
            
            user.account_status = data.user_information.account_status
            user.full_name = data.user_information.full_name if data.user_information.full_name else user.full_name
            user.role = data.user_information.role if data.user_information.role else user.role

            await session.commit()
            await session.refresh(user)
            return AdminUpdateUserResponse(
                code=200, 
                message='User Information Updated', 
                full_name=user.full_name, 
                role=user.role, 
                account_status=user.account_status
            )
        except Exception as e:
            print(f'User Controller Exception:\n{e}')
            return ServerSideErrorResponse()
        
    @staticmethod
    async def get_pendings(
        session:AsyncSession | None
    ):
        try:
            if session is None: raise Exception()

            stmt = select(UserModel).where(
                UserModel.account_status == "PENDING"
            )

            res:Result = await session.execute(stmt)
            pendings:list[UserModel]= res.scalars().all()

            if not pendings: return PendingAccountsResponse(code=404, message='No Pending Accounts')

            accounts:list[PendingAccountsInformation] = []
            for p in pendings:
                accounts.append(
                    PendingAccountsInformation(
                        id=p._id,
                        full_name=p.full_name,
                        email=p.email,
                        account_status=p.account_status,
                        role=p.role,
                        created_at=p.created_at.strftime('%y-%m-%d %H:%M:%S')
                    )
                )
            return PendingAccountsResponse(code=200, message='Pending Accounts Gathered', pending_accounts=accounts)
        except Exception as e:
            print(f'User Controller Exception:\n{e}')
            return ServerSideErrorResponse()
        

    @staticmethod
    async def get_users(
        page:int,
        session:AsyncSession | None
    ):
        try:
            if session is None: raise Exception()

            limit:int = 10
            offset:int = (page - 1) * limit

            stmt = select(UserModel).where(
                (UserModel.role != 3) &
                (UserModel.account_status!="DISABLED")
            ).limit(limit).offset(offset)

            res:Result = await session.execute(stmt)
            pendings:list[UserModel]= res.scalars().all()

            if not pendings: return PendingAccountsResponse(code=404, message='No Accounts Yet')

            count=select(func.count()).select_from(UserModel).where(
                (UserModel.role != 3) &
                (UserModel.account_status!="DISABLED")
            )

            count_res:Result=await session.execute(count)
            total= count_res.scalar_one_or_none()
            if not total: total = 0
            total= max((total + limit-1)//limit, 1)

            accounts:list[PendingAccountsInformation] = []
            for p in pendings:
                accounts.append(
                    PendingAccountsInformation(
                        id=p._id,
                        full_name=p.full_name,
                        email=p.email,
                        account_status=p.account_status,
                        role=p.role,
                        created_at=p.created_at.strftime('%y-%m-%d %H:%M:%S')
                    )
                )
            return UserAccountsResponse(code=200, message='Users Accounts Gathered', accounts=accounts, pages=total)
        except Exception as e:
            print(f'User Controller Exception:\n{e}')
            return ServerSideErrorResponse()

    @staticmethod
    async def forget_password(
        data:ForgetPasswordRequest,
        session:AsyncSession | None
    ):
        try:
            if session is None: raise Exception('Session is not Initialized')

            stmt = select(UserModel).where(UserModel.email == data.email)
            res:Result = await session.execute(stmt)
            user:UserModel = res.scalar_one_or_none()

            if not user: return ForgetPasswordResponse(code=404, message='Account is not Registered')
            if user.role != None and user.role == 3: return ForgetPasswordResponse(code=401, message='Not allowed')

            stmt= select(ForgetPasswordTokenModel).where(
                ForgetPasswordTokenModel.email == data.email
            )
            res = await session.execute(stmt)

            fpt:ForgetPasswordTokenModel = res.scalar_one_or_none()

            if fpt:
                if not fpt.is_expired():
                    return ForgetPasswordResponse(code=200, message='Reset Password link is already sent!')

            to_insert:ForgetPasswordTokenModel = ForgetPasswordTokenModel()
            to_insert.token = secrets.token_urlsafe(64)
            to_insert.email = data.email
            to_insert.exp = (datetime.now(timezone('Asia/Riyadh')) + timedelta(hours=1)).replace(tzinfo=None)

            session.add(to_insert)
            await session.commit()
            # send
            mailutil=MailUtil()
            await mailutil.send_reset(to=to_insert.email, link=f'https://ruyai.hive-sa.dev/{to_insert.token}')

            return ForgetPasswordResponse(code=200, message='Reset Password Link Sent to Your Email')
        except Exception as e:
            print(f'User Controller Exception:\n{e}')
            return ServerSideErrorResponse()
        
    @staticmethod
    async def reset_password(
        token:str,
        data:ResetPasswordRequest,
        session:AsyncSession | None
    ):
        try:
            if session is None: raise Exception('Session is not Initialized')

            stmt=select(ForgetPasswordTokenModel).where(ForgetPasswordTokenModel.token == token)
            res:Result = await session.execute(stmt)
            fpt:ForgetPasswordTokenModel = res.scalar_one_or_none()
            if not fpt: return ResetPasswordResponse(code=403, message='Invalid Token')

            if fpt.is_expired(): return ResetPasswordResponse(code=403, message='Expired Token')
            
            stmt=select(UserModel).where(UserModel.email == fpt.email)
            res = await session.execute(stmt)
            user:UserModel = res.scalar_one_or_none()

            if not user: return ResetPasswordResponse(code=403, message='Invalid Token')

            hashed:str = HashHelper.hash_with_salt(password=data.new_password, salt=user.salt)

            user.password = hashed

            await session.delete(fpt)
            await session.commit()
            await session.refresh(user)
            return ResetPasswordResponse(code=200, message='Password was updated successfully')
        except Exception as e:
            print(f'User Controller Exception:\n{e}')
            return ServerSideErrorResponse()