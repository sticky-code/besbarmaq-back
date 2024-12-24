import uuid
from typing import Sequence

from litestar import Controller, get, patch, post, status_codes
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models import Room, User
from src.schemas import CreateRoomDTO, PartialDTO
from src.types import RoomStatusType


class RoomController(Controller):
    path = '/rooms'

    @post('/')
    async def create_room(self, db_session: AsyncSession, data: CreateRoomDTO, user_id: int) -> dict:
        user = await db_session.get(User, user_id)
        room = Room(
            host_id=user_id,
            password=data.password,
            name=data.name,
        )
        room.users.append(user)

        db_session.add(room)
        await db_session.commit()
        await db_session.refresh(room)

        return {'room_id': room.id}

    @patch('/{room_id: uuid}', dto=PartialDTO[Room], status_code=status_codes.HTTP_200_OK)
    async def patch_room(
            self, user_id: int, db_session: AsyncSession, room_id: uuid.UUID, data: Room,
    ) -> dict:
        room = (await db_session.execute(
            select(Room)
            .filter_by(id=room_id)
        )).scalars().first()

        if room:
            room.status = data.status or room.status
            room.password = data.password or room.password
            room.name = data.name or room.name
            room.host_id = user_id

            await db_session.commit()
            await db_session.refresh(room)
            return {
                'id': room.id,
                'status': room.status,
                'name': room.name,
                'host_id': room.host_id,
            }

        raise HTTPException(status_code=404, detail='Room not found')

    @get('/', status_code=status_codes.HTTP_200_OK)
    async def list_rooms(self, user_id: int, db_session: AsyncSession) -> Sequence[dict]:
        rooms = (await db_session.execute(
            select(Room)
            .options(joinedload(Room.users))
            .filter_by(status=RoomStatusType.OPEN)
        )).unique().scalars().all()

        return [
            {
                'id': room.id,
                'name': room.name,
                'host_id': room.host_id,
                'status': room.status,
                'user_count': len(room.users),
                'is_passworded': bool(room.password),
            }
            for room in rooms
        ]
