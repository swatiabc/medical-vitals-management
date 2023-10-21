import datetime
import unittest

from exception.exception import ValidationError
from models.user import User, Gender
from models.vital import VitalId, Vital
from repo.user import UserRepo
from repo.vital import VitalRepo
from services.aggregation import AggregationService
from services.user import UserService
from services.vital import VitalService
from view.aggregate import AggregateView


class TestAggregateView(unittest.TestCase):
    def setUp(self):
        self.user_repo = UserRepo()
        self.vital_repo = VitalRepo()
        self.user_service = UserService(self.user_repo)
        self.vital_service = VitalService(self.vital_repo, self.user_repo)
        self.aggregation_service = AggregationService(
            self.user_service, self.vital_service
        )

    def test_aggregate_no_vitals(self):
        command = {
            "command": "aggregate",
            "username": "swati",
            "vital_ids": ["HEART_RATE", "TEMPERATURE"],
            "start_timestamp": "2023-10-01 00:00:00",
            "end_timestamp": "2023-10-31 23:59:59",
        }

        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )
        vital_id = VitalId.TEMPERATURE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )
        view = AggregateView(
            self.user_service, self.vital_service, self.aggregation_service
        )
        with self.assertRaises(ValidationError) as context:
            response = view.aggregate(command)
        self.assertEqual(
            context.exception.args[0],
            "vital id not present for vital id: HEART_RATE and "
            "timestamp 2023-10-01 00:00:00 - 2023-10-31 23:59:59",
        )

    def test_aggregate(self):
        command = {
            "command": "aggregate",
            "username": "swati",
            "vital_ids": ["HEART_RATE", "TEMPERATURE"],
            "start_timestamp": "2022-10-01 00:00:00",
            "end_timestamp": "2024-10-31 23:59:59",
        }

        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )
        vital_id = VitalId.TEMPERATURE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )

        view = AggregateView(
            self.user_service, self.vital_service, self.aggregation_service
        )
        response = view.aggregate(command)
        self.assertEqual(
            response.get("data").get("aggregates"),
            {"HEART_RATE": 77.5, "TEMPERATURE": 77.5},
        )

    def test_insight_no_data(self):
        command = {
            "command": "aggregate",
            "username": "swati",
            "vital_id": "TEMPERATURE",
            "start_timestamp": "2023-10-01 00:00:00",
            "end_timestamp": "2023-10-31 23:59:59",
        }

        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )
        vital_id = VitalId.TEMPERATURE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )

        view = AggregateView(
            self.user_service, self.vital_service, self.aggregation_service
        )
        with self.assertRaises(ValidationError) as context:
            response = view.population_insight(command)
        self.assertEqual(
            "vital id not present for vital id: TEMPERATURE and "
            "timestamp 2023-10-01 00:00:00 - 2023-10-31 23:59:59",
            context.exception.args[0],
        )

    def test_insight_single_user(self):
        command = {
            "command": "aggregate",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "start_timestamp": "2022-10-01 00:00:00",
            "end_timestamp": "2024-10-31 23:59:59",
        }

        user = User("swati", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )
        vital_id = VitalId.TEMPERATURE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )

        view = AggregateView(
            self.user_service, self.vital_service, self.aggregation_service
        )
        response = view.population_insight(command)
        self.assertEqual(
            response.get("data").get("insight"),
            "Your HeartRate is in the 100.0 percentile.",
        )

    def test_insight_multiple_user(self):
        command = {
            "command": "aggregate",
            "username": "swati",
            "vital_id": "HEART_RATE",
            "start_timestamp": "2022-10-01 00:00:00",
            "end_timestamp": "2024-10-31 23:59:59",
        }

        user = User("swati", 30, Gender.FEMALE, [])

        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )

        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user.username, vital_id, 75, timestamp1)
        vital2 = Vital(user.username, vital_id, 80, timestamp2)
        self.vital_service.create_vital(
            user.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user.username, vital_id, vital2.value, vital2.timestamp
        )

        user2 = User("shivam", 40, Gender.MALE, [])
        self.user_service.create_user(
            user2.username, user2.age, user2.gender, user2.illness
        )
        vital1 = Vital(user2.username, vital_id, 80, timestamp1)
        vital2 = Vital(user2.username, vital_id, 100, timestamp2)
        self.vital_service.create_vital(
            user2.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user2.username, vital_id, vital2.value, vital2.timestamp
        )

        view = AggregateView(
            self.user_service, self.vital_service, self.aggregation_service
        )
        response = view.population_insight(command)
        self.assertEqual(
            response.get("data").get("insight"),
            "Your HeartRate is in the 50.0 percentile.",
        )


if __name__ == "__main__":
    unittest.main()
