"""
Purpose: To add User data into inmemory database (dictionary)
No complicated business logic is required or added here
Will use a dictionary to store User instances, where key: username and value: User instance
"""

from models.user import User


class UserRepo:
    def __init__(self) -> None:
        self.__users = {}

    @property
    def users(self) -> dict:
        """

        :return: {key (username): value (User instance)}
        """
        return self.__users

    def create(self, user: User) -> None:
        """
        :param user:
        :return:
        """
        self.__users[user.username] = user

    def retrieve(self, user_name: str) -> User:
        """
        :param user_name:
        :return:
        """
        return self.__users.get(user_name)
