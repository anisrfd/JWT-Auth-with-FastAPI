from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    """
    JWTBearer class is responsible to check
    whether the request is authorized or
    not [verification of the protected route]
    """
    def __init__(self, auto_error: bool = True):
        """
        Initialization method of JWTBearer

        :param auto_error: bool object
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Takes request and verify JWT

        :param request: Request object
        :return: credentials or raise HTTPException
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self._is_verified(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def _is_verified(self, jwToken: str) -> bool:
        """
        Takes jwToken and verify it by decoding

        :param jwToken: str object
        :return: bool object
        """
        try:
            payload = decode_jwt(jwToken)
        except:
            payload = None
        return True if payload else False
