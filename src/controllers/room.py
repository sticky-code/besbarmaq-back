from typing import Sequence
from uuid import UUID

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from litestar import Controller, Response, get, post
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.models import Room, User, user_rooms_association
from src.schemas import CreateRoomDTO
from src.types import RoomStatusType


class RoomController(Controller):
    path = '/rooms'

    @get('/{room_id: uuid}')
    async def room_details(self, room_id: UUID) -> None: ...

    @post('/')
    async def create_room(self, user_id: int, db_session: AsyncSession, data: CreateRoomDTO) -> Response:
        user = await db_session.get(User, user_id)
        room = Room(host=user, password=data.password)
        room.users.append(user)
        db_session.add(room)
        await db_session.commit()
        await db_session.refresh(room)

        return Response({'room_id': room.id})

    @get('/', return_dto=SQLAlchemyDTO[Room])
    async def list_rooms(self, user_id: int, db_session: AsyncSession) -> Sequence[Room]:
        user_rooms = aliased(user_rooms_association)

        result = await db_session.execute(
            select(Room)
            .join(user_rooms, Room.id == user_rooms.c.room_id)
            .group_by(Room.id)
            .having(func.count(user_rooms.c.user_id) > 0)
            .filter(Room.status == RoomStatusType.OPEN)
        )

        return result.scalars().all()
