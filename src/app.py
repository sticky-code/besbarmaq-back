import uvicorn
from litestar import Litestar
from litestar.di import Provide
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin

from src.config import settings
from src.dependencies import get_user_id
from src.routes import routes

db_config = SQLAlchemyAsyncConfig(connection_string=str(settings.database_url))

app = Litestar(
    route_handlers=routes,
    plugins=[SQLAlchemyInitPlugin(config=db_config)],
    debug=True,
    dependencies={'user_id': Provide(get_user_id)}
)


if __name__ == '__main__':
    uvicorn.run('src.app:app', host='0.0.0.0', port=8000, reload=True)
