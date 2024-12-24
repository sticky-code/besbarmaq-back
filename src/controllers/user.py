from litestar import Controller, get, status_codes
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import User
from src.schemas import UserDTO


class UserController(Controller):
    path = '/users'

    @get('/{other_user_id:int}', status_code=status_codes.HTTP_200_OK, return_dto=UserDTO)
    async def get_user(self, user_id: int, other_user_id: int, db_session: AsyncSession) -> User:
        user = (await db_session.execute(
            select(User)
            .filter_by(id=other_user_id)
            .options(
                joinedload(User.statistics),
                joinedload(User.room_history),
            )
        )).unique().scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status_codes.HTTP_404_NOT_FOUND)

        return user

    @get('/me', status_code=status_codes.HTTP_200_OK, return_dto=UserDTO)
    async def get_me(self, user_id: int, db_session: AsyncSession) -> User:
        user = (await db_session.execute(
            select(User)
            .filter_by(id=user_id)
            .options(
                joinedload(User.statistics),
                joinedload(User.room_history),
            )
        )).unique().scalar_one_or_none()

        return user
