import datetime


class BaseModel:
    def __init__(self) -> None:
        self.__created_at = datetime.datetime.now()
        self.__updated_at = datetime.datetime.now()

    @property
    def created_at(self) -> datetime.datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime.datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value: datetime.datetime) -> None:
        self.__updated_at = value
