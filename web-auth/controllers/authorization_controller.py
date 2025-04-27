from utility import TokenHelper

from views import (
    VerifyTokenRequest,
    VerifyTokenResponse,
)

class AuthorizationController:
    @staticmethod
    async def verify(data:VerifyTokenRequest)->VerifyTokenResponse:
        payload, isValid= TokenHelper.verify(token=data.token)
        if not isValid:
            return VerifyTokenResponse(
                code=403,
                message='Invalid access token',
                valid=isValid
            )
        return VerifyTokenResponse(
            code=200,
            message='Valid access token',
            valid=isValid,
            id=payload.get('_id'),
            full_name=payload.get('full_name'),
            role=payload.get('role'),
        )