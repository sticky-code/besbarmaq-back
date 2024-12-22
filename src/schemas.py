from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig
from pydantic import BaseModel


class ExcludeIdDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(exclude={'id'})


class ExcludeIdAndTimestampsDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(exclude={'id', 'created_at', 'updated_at'})


class AuthDTO(BaseModel):
    username: str
    password: str


class CreateRoomDTO(BaseModel):
    password: str | None = None
