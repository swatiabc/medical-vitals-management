import unittest

from exception.exception import ObjectNotFound, DuplicateObject
from models.user import User, Gender
from repo.user import UserRepo
from services.user import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        # Initialize a UserRepo and a UserService instance before each test
        self.user_repo = UserRepo()
        self.user_service = UserService(self.user_repo)

    def test_create_user(self):
        # Create a user and verify it can be retrieved
        user_name = "swati"
        user_age = 30
        user_gender = Gender.FEMALE
        user_illness = ["Flu"]
        self.user_service.create_user(user_name, user_age, user_gender, user_illness)
        retrieved_user = self.user_service.retrieve_user(user_name)

        self.assertEqual(retrieved_user.username, user_name)
        self.assertEqual(retrieved_user.age, user_age)
        self.assertEqual(retrieved_user.gender, user_gender)
        self.assertEqual(retrieved_user.illness, user_illness)

    def test_create_user_with_existing_username(self):
        # Attempt to create a user with an existing username (should raise an exception)
        user_name = "swati"
        user_age = 30
        user_gender = Gender.FEMALE
        user_illness = ["Flu"]
        self.user_service.create_user(user_name, user_age, user_gender, user_illness)

        with self.assertRaises(Exception) as context:
            self.user_service.create_user(user_name, 25, Gender.MALE, [])

        self.assertIsInstance(context.exception, DuplicateObject)

    def test_retrieve_nonexistent_user(self):
        # Retrieve a user that does not exist (should raise an exception)
        with self.assertRaises(Exception) as context:
            self.user_service.retrieve_user("nonexistent")

        self.assertIsInstance(context.exception, ObjectNotFound)


if __name__ == "__main__":
    unittest.main()
