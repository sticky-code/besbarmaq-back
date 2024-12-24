import uuid

import bcrypt
from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.types import RoomStatusType


class Base(DeclarativeBase): ...


user_rooms_association = Table(
    'user_rooms_association',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE')),
    Column('room_id', UUID, ForeignKey('rooms.id', ondelete='CASCADE')),
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    statistics: Mapped['Statistic'] = relationship('Statistic', back_populates='user', uselist=False)
    room_history: Mapped[list['Room']] = relationship(
        'Room',
        secondary=user_rooms_association,
        back_populates='users',
    )

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())


class Statistic(Base):
    __tablename__ = 'statistics'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='statistics')
    overall_wpm: Mapped[int] = mapped_column()
    overall_accuracy: Mapped[float] = mapped_column()


class RoomStatistic(Base):
    __tablename__ = 'room_statistics'

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'))
    room: Mapped['Room'] = relationship(back_populates='statistics')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    wpm: Mapped[int] = mapped_column()
    accuracy: Mapped[float] = mapped_column()


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    host_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    users: Mapped[list['User']] = relationship(
        'User',
        secondary=user_rooms_association,
        back_populates='room_history',
    )
    statistics: Mapped[list['RoomStatistic']] = relationship('RoomStatistic', back_populates='room')
    status: Mapped[RoomStatusType] = mapped_column(Enum(RoomStatusType), default=RoomStatusType.OPEN)
    password: Mapped[str] = mapped_column(nullable=True, default=None)
