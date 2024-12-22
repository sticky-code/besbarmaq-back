from datetime import UTC, datetime, timedelta

import jwt
from litestar import Controller, Response, post, status_codes
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models import User
from src.schemas import AuthDTO


class AuthController(Controller):
    path = '/auth'

    @post('/login')
    async def login(self, db_session: AsyncSession, data: AuthDTO) -> Response:
        user = (
            await db_session.execute(select(User).filter(User.username == data.username))
        ).scalar_one_or_none()

        if not (user and user.check_password(data.password)):
            raise HTTPException(
                status_code=status_codes.HTTP_400_BAD_REQUEST, detail='Invalid username or password',
            )

        return Response(
            {'token': self.generate_token({'user_id': user.id})},
            status_code=status_codes.HTTP_200_OK,
        )

    @post('/register')
    async def register(self, db_session: AsyncSession, data: AuthDTO) -> Response:
        try:
            user = User(username=data.username)
            user.set_password(data.password)
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
        except IntegrityError:
            raise HTTPException(status_code=status_codes.HTTP_400_BAD_REQUEST, detail='User already exists')

        return Response({'token': self.generate_token({'user_id': user.id})})

    def generate_token(self, payload: dict):
        payload['exp'] = datetime.now(UTC) + timedelta(seconds=settings.jwt_expiration)

        return jwt.encode(payload, settings.secret_key)

