from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.engine import Result
from models import RoleModel
from views import AllowedRolesResponse, ServerSideErrorResponse, Role

class RoleController:

    @staticmethod
    async def get_allowed_roles(
        session:AsyncSession|None
    )->AllowedRolesResponse:
        try:
            if session is None: raise Exception('Session is not Initialized')
            stmt=select(RoleModel).where(
                RoleModel.role.notilike("%admin%")
            )
            print('enter')
            res:Result = await session.execute(stmt)
            print('executed')

            roles:list[RoleModel]= res.scalars().all()
            if not roles: return AllowedRolesResponse(code=404, message='No Roles Available')
            print('not null')

            _rols:list[Role] = [Role(id=r._id, role=r.role) for r in roles]
            
            return AllowedRolesResponse(code=200, message='Successfully get allowed roles', roles=_rols)
        except Exception as e:
            print(f'Role controller exception:\n{e}')
            return ServerSideErrorResponse()
    
    @staticmethod
    async def check_valid_role(
        role:int,
        session:AsyncSession|None
    )-> bool:
        try:
            if session is None: raise Exception()

            stmt=select(RoleModel).where((RoleModel._id == role)& (RoleModel.role.notilike('%admin%')))
            res:Result = await session.execute(stmt)
            isValid = res.scalar_one_or_none()
            if not isValid: return False
            return True
        except Exception as e:
            print(f'Role controller exception:\n{e}')
            return False
    
    @staticmethod
    async def get_role_name(
        role:int,
        session:AsyncSession|None
    )->str|None:
        try:
            if session is None: raise Exception()
            stmt=select(RoleModel).where(RoleModel._id == role)
            res:Result = await session.execute(stmt)
            role:RoleModel = res.scalar_one_or_none()
            if not role: return None
            return role.role
        except Exception as e:
            print(f'Role controller exception:\n{e}')
            return None
        
    @staticmethod
    async def is_admin(
        role:int,
        session:AsyncSession|None
    )-> bool:
        try:
            if session is None: raise Exception()

            stmt=select(RoleModel).where((RoleModel._id == role))
            res:Result = await session.execute(stmt)
            role:RoleModel = res.scalar_one_or_none()
            if not role: return False
            return (role.role.upper() == "ADMIN")
        except Exception as e:
            print(f'Role controller exception:\n{e}')
            return False