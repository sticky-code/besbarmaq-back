import uuid

from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from pydantic import BaseModel

from src.models import User


class ExcludeIdDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(exclude={'id'})


class ExcludeIdAndTimestampsDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(exclude={'id', 'created_at', 'updated_at'})


class PartialDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(partial=True)


class AuthDTO(BaseModel):
    username: str
    password: str


class CreateRoomDTO(BaseModel):
    name: str
    password: str | None = None


class UpdateStatisticDTO(BaseModel):
    room_id: uuid.UUID
    wpm: int
    accuracy: float


class UserDTO(SQLAlchemyDTO[User]):
    config = SQLAlchemyDTOConfig(exclude={'hashed_password'}, partial=True)
