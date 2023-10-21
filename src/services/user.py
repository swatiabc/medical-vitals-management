"""
UserService interacts with UserRepo for create and retrieve operations.
All the business logic and validation checks are present here
"""

from exception.exception import DuplicateObject, ObjectNotFound
from models.user import User, Gender
from repo.user import UserRepo


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.repo = user_repo

    def create_user(
        self, user_name: str, age: int, gender: Gender, illness: list
    ) -> None:
        """

        :param user_name:
        :param age:
        :param gender:
        :param illness:
        :return:
        Function to create User using UserRepo
        """
        if self.repo.retrieve(user_name):
            raise DuplicateObject(model_name=User, user_name=user_name)

        user = User(username=user_name, age=age, gender=gender, illness=illness)
        self.repo.create(user)

    def retrieve_user(self, user_name: str) -> User:
        """

        :param user_name:
        :return:
        To retrieve user information from the given user name
        """
        user = self.repo.retrieve(user_name)
        if not user:
            raise ObjectNotFound(model_name=User, user_name=user_name)
        return user
