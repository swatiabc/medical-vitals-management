import datetime
from enum import Enum

from models.base import BaseModel
from models.user import User


class VitalId(str, Enum):
    HEART_RATE = "HEART_RATE"
    TEMPERATURE = "TEMPERATURE"


class Vital(BaseModel):
    def __init__(
        self,
        user_name: User.username,
        vital_id: VitalId,
        value: int,
        timestamp: datetime.datetime,
    ) -> None:
        super(Vital).__init__()
        self.__id = None
        self.__user_name = user_name
        self.__vital_id = vital_id
        self.__value = value
        self.__timestamp = timestamp

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, data: int):
        self.__id = data

    @property
    def vital_id(self) -> VitalId:
        return self.__vital_id

    @property
    def value(self) -> int:
        return self.__value

    @property
    def timestamp(self) -> datetime.datetime:
        return self.__timestamp

    @property
    def user_name(self):
        return self.__user_name

    @value.setter
    def value(self, data: int) -> None:
        self.__value = data
