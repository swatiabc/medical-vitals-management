import unittest

from exception.exception import DuplicateObject, ObjectNotFound
from models.user import User, Gender
from repo.user import UserRepo
from services.user import UserService
from view.user import UserView


class TestUserView(unittest.TestCase):
    def setUp(self) -> None:
        self.user_repo = UserRepo()
        self.user_service = UserService(self.user_repo)

    def test_create_user(self):
        command = {
            "command": "create_user",
            "username": "Alice",
            "age": 25,
            "gender": "Female",
        }

        view = UserView(self.user_service)
        response = view.create_user(command)
        self.assertIsInstance(self.user_service.repo.users.get("Alice"), User)
        self.assertEqual(response.get("status"), "success")
        self.assertEqual(response.get("message"), "User Alice created successfully.")

    def test_create_duplicate_user(self):
        user = User("swati", 30, Gender.FEMALE, [])

        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        command = {
            "command": "create_user",
            "username": "swati",
            "age": 25,
            "gender": "Female",
        }

        view = UserView(self.user_service)
        with self.assertRaises(DuplicateObject) as context:
            response = view.create_user(command)

    def test_get_user(self):
        user = User("swati", 30, Gender.FEMALE, [])

        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        command = {
            "command": "get_user",
            "username": "swati",
        }
        view = UserView(self.user_service)
        response = view.get_user(command)
        self.assertEqual(
            {"user_name": "swati", "age": 30, "gender": "female", "illness": []},
            response.get("data"),
        )

    def test_get_user_no_entry(self):
        command = {
            "command": "get_user",
            "username": "swati",
        }
        view = UserView(self.user_service)

        with self.assertRaises(ObjectNotFound):
            response = view.get_user(command)


if __name__ == "__main__":
    unittest.main()
