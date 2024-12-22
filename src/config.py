from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: PostgresDsn
    secret_key: str
    jwt_expiration: int
    jwt_algorithm: str = 'HS256'


settings = Settings()

