from enum import StrEnum, auto, unique


@unique
class RoomStatusType(StrEnum):
    OPEN = auto()
    CLOSED = auto()
    IN_PROGRESS = auto()
