import unittest
from models.user import User, Gender  # Import your UserRepo implementation
from repo.user import UserRepo


class TestUserRepo(unittest.TestCase):
    def setUp(self):
        self.user_repo = UserRepo()

    def test_create_user(self):
        # Create a user and verify it can be retrieved
        user = User(
            username="swati",
            age=24,
            gender=Gender.FEMALE.value,
            illness=["fever", "high bp"],
        )
        self.user_repo.create(user)
        retrieved_user = self.user_repo.retrieve("swati")
        self.assertEqual(retrieved_user, user)

    def test_retrieve_user(self):
        # Retrieve a user that does not exist in the repository
        user = self.user_repo.retrieve("nonexistent")
        self.assertIsNone(user)  # The user should not be found

    def test_create_and_retrieve_multiple_users(self):
        # Create and retrieve multiple users
        users = [
            User(username="KESHAV", age=27, gender=Gender.MALE.value),
            User(username="jyoti", age=56, gender=Gender.FEMALE.value),
            User(username="shivam", age=15, gender=Gender.MALE.value),
        ]

        for user in users:
            self.user_repo.create(user)

        for user in users:
            retrieved_user = self.user_repo.retrieve(user.username)
            self.assertEqual(retrieved_user, user)


if __name__ == "__main__":
    unittest.main()
