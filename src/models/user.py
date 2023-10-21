from enum import Enum

from models.base import BaseModel


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class User(BaseModel):
    def __init__(
        self, username: str, age: int, gender: Gender, illness: list = None
    ) -> None:
        if illness is None:
            illness = list()
        super(User).__init__()
        self.__username = username
        self.__age = age
        self.__gender = gender
        self.__illness = illness

    @property
    def username(self) -> str:
        return self.__username

    @property
    def age(self) -> int:
        return self.__age

    @property
    def gender(self) -> Gender:
        return self.__gender

    @property
    def illness(self) -> list:
        return self.__illness
