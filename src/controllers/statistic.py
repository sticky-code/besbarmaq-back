from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from litestar import Controller, Response, get, post, status_codes
from litestar.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Room, RoomStatistic, Statistic
from src.schemas import UpdateStatisticDTO
from src.types import RoomStatusType


class StatisticController(Controller):
    path = '/statistics'

    @get('/', status_code=status_codes.HTTP_200_OK, return_dto=SQLAlchemyDTO[Statistic])
    async def get_statistics(self, user_id: int, db_session: AsyncSession) -> Statistic:
        result = await db_session.execute(
            select(Statistic)
            .filter(Statistic.user_id == user_id)
        )
        statistics = result.scalars().first()

        if statistics is None:
            raise HTTPException(status_code=404, detail='Statistics not found')

        return statistics

    @post('/', status_code=status_codes.HTTP_200_OK)
    async def update_statistics(
            self, user_id: int, db_session: AsyncSession, data: UpdateStatisticDTO,
    ) -> Response:
        new_room_statistic = RoomStatistic(
            room_id=data.room_id,
            user_id=user_id,
            wpm=data.wpm,
            accuracy=data.accuracy
        )

        room_statistics = (await db_session.execute(
            select(RoomStatistic)
            .join(Room, Room.id == RoomStatistic.room_id)
            .filter(RoomStatistic.user_id == user_id, Room.status == RoomStatusType.CLOSED)
        )).scalars().all()

        total_wpm = sum(stat.wpm for stat in room_statistics) + data.wpm
        total_accuracy = sum(stat.accuracy for stat in room_statistics) + data.accuracy

        overall_wpm = total_wpm / (len(room_statistics) + 1)
        overall_accuracy = total_accuracy / (len(room_statistics) + 1)

        try:
            statistics = (await db_session.execute(
                select(Statistic)
                .filter(Statistic.user_id == user_id)
            )).scalar_one()
        except NoResultFound:
            statistics = Statistic(user_id=user_id)

        statistics.overall_wpm = overall_wpm
        statistics.overall_accuracy = overall_accuracy

        db_session.add_all([statistics, new_room_statistic])
        await db_session.commit()

        return Response(status_code=status_codes.HTTP_200_OK, content={})
