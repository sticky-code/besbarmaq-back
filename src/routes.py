from litestar import Response, get, status_codes

from src.controllers import AuthController, RoomController, StatisticController, UserController


@get('/health/')
async def health() -> Response:
    return Response(content={}, status_code=status_codes.HTTP_200_OK)


routes = [health, AuthController, RoomController, UserController, StatisticController]
