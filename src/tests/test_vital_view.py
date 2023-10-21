import datetime
import unittest

from exception.exception import ObjectNotFound
from models.user import User, Gender
from models.vital import VitalId, Vital
from repo.user import UserRepo
from repo.vital import VitalRepo
from services.user import UserService
from services.vital import VitalService
from utils.rb_tree.execute import RedBlackExecuter
from view.vital import VitalView


class TestUserView(unittest.TestCase):
    def setUp(self) -> None:
        self.user_repo = UserRepo()
        self.vital_repo = VitalRepo()
        self.user_service = UserService(self.user_repo)
        self.vital_service = VitalService(self.vital_repo, self.user_repo)

    def test_insert_vital(self):
        command = {
            "command": "insert_vital",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "value": 105,
            "timestamp": "2023-10-04 10:00:00",
        }
        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        view = VitalView(self.user_service, self.vital_service)
        response = view.insert_vital(command)
        self.assertEqual(
            response.get("message"), "Vital HEART_RATE for swati inserted successfully."
        )
        self.assertIsInstance(
            self.vital_service.vital_repo.vitals.get("swati").get("HEART_RATE"),
            RedBlackExecuter,
        )

    def test_multiple_insert(self):
        commands = [
            {
                "command": "insert_vital",
                "username": "swati",
                "vital_id": "HEART_RATE",
                "value": 105,
                "timestamp": "2023-10-04 10:00:00",
            },
            {
                "command": "insert_vital",
                "username": "swati",
                "vital_id": "TEMPERATURE",
                "value": 105,
                "timestamp": "2023-10-04 10:00:00",
            },
        ]
        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        view = VitalView(self.user_service, self.vital_service)
        for command in commands:
            view.insert_vital(command)
        rb_tree_heart_rate = self.vital_service.vital_repo.vitals.get("swati").get(
            "HEART_RATE"
        )
        rb_tree_temp = self.vital_service.vital_repo.vitals.get("swati").get(
            "TEMPERATURE"
        )
        self.assertIsInstance(rb_tree_temp, RedBlackExecuter)
        self.assertIsInstance(rb_tree_heart_rate, RedBlackExecuter)

    def test_user_not_present(self):
        command = {
            "command": "insert_vital",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "value": 105,
            "timestamp": "2023-10-04 10:00:00",
        }
        view = VitalView(self.user_service, self.vital_service)

        with self.assertRaises(ObjectNotFound):
            response = view.insert_vital(command)

    def test_get_vital(self):
        command = {
            "command": "get_vitals",
            "username": "swati",
            "period": ["2022-10-04 10:00:00", "2024-10-05 10:00:00"],
        }
        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        timestamp3 = datetime.datetime(2020, 1, 1, 11, 0)
        timestamp4 = datetime.datetime(2023, 2, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        vital3 = Vital(user.username, vital_id, 80, timestamp3)
        vital4 = Vital(user.username, vital_id, 80, timestamp4)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital3.value, vital3.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital4.value, vital4.timestamp
        )
        view = VitalView(self.user_service, self.vital_service)
        response = view.get_vitals(command)
        self.assertEqual(3, len(response.get("data")))

    def test_get_value_data_not_present(self):
        command = {
            "command": "get_vitals",
            "username": "swati",
            "period": ["2022-10-04 10:00:00", "2024-10-05 10:00:00"],
        }
        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        view = VitalView(self.user_service, self.vital_service)
        response = view.get_vitals(command)
        self.assertEqual(response.get("data"), [])

    def test_user_not_present(self):
        command = {
            "command": "get_vitals",
            "username": "swati",
            "period": ["2022-10-04 10:00:00", "2024-10-05 10:00:00"],
        }
        view = VitalView(self.user_service, self.vital_service)
        response = view.get_vitals(command)
        self.assertEqual(response.get("data"), [])

    def test_update_vital(self):
        command = {
            "command": "update_vital",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "timestamp": "2023-10-03 14:30:00",
            "value": 89,
        }
        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp = datetime.datetime(2023, 10, 3, 14, 30)
        vital = Vital(user.username, vital_id, 75, timestamp)
        self.vital_service.create_vital(
            user.username, vital_id, vital.value, vital.timestamp
        )
        view = VitalView(self.user_service, self.vital_service)
        response = view.update_vital(command)
        self.assertEqual(
            self.vital_service.vital_repo.vitals.get("swati")
            .get(VitalId.HEART_RATE)
            .root.instance.value,
            command.get("value"),
        )

    def test_update_vital_no_data(self):
        command = {
            "command": "update_vital",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "timestamp": "2022-10-03 14:30:00",
            "value": 89,
        }
        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp = datetime.datetime(2023, 10, 3, 14, 30)
        vital = Vital(user.username, vital_id, 75, timestamp)
        self.vital_service.create_vital(
            user.username, vital_id, vital.value, vital.timestamp
        )
        view = VitalView(self.user_service, self.vital_service)
        with self.assertRaises(ObjectNotFound):
            view.update_vital(command)

    def test_update_vital_no_user(self):
        command = {
            "command": "update_vital",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "timestamp": "2022-10-03 14:30:00",
            "value": 89,
        }
        view = VitalView(self.user_service, self.vital_service)
        with self.assertRaises(ObjectNotFound):
            view.update_vital(command)


if __name__ == "__main__":
    unittest.main()
