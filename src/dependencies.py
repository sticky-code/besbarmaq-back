import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from litestar import Request, status_codes
from litestar.exceptions import HTTPException

from src.config import settings


async def get_user_id(request: Request) -> int:
    token = request.headers.get('Authorization')

    if not token:
        raise HTTPException(status_code=status_codes.HTTP_401_UNAUTHORIZED)

    token = token.split()[-1]

    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])['user_id']
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token has expired')
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
