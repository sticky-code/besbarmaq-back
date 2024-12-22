import uuid

import bcrypt
from sqlalchemy import UUID, Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.types import RoomStatusType


class Base(DeclarativeBase):
    pass


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
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    statistics: Mapped['Statistic'] = relationship('Statistic', back_populates='user')

    def set_password(self, password: str) -> None:
        self.hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password.encode())

    def __repr__(self) -> str:
        return self.username


class Statistic(Base):
    __tablename__ = 'statistics'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='statistics')
    wpm: Mapped[int] = mapped_column()
    accuracy: Mapped[float] = mapped_column()


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    host_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    host: Mapped['User'] = relationship('User', backref='hosted_rooms')
    users: Mapped[list['User']] = relationship('User', secondary=user_rooms_association, backref='rooms')
    status: Mapped[RoomStatusType] = mapped_column(Enum(RoomStatusType), default=RoomStatusType.OPEN)
    password: Mapped[str] = mapped_column(nullable=True, default=None)
