import unittest
import datetime

from exception.exception import ObjectNotFound
from models.user import User, Gender
from models.vital import VitalId, Vital
from services.aggregation import AggregationService
from services.user import UserService
from services.vital import VitalService
from repo.user import UserRepo
from repo.vital import VitalRepo


class TestAggregationService(unittest.TestCase):
    def setUp(self):
        self.user_repo = UserRepo()
        self.vital_repo = VitalRepo()
        self.user_service = UserService(self.user_repo)
        self.vital_service = VitalService(self.vital_repo, self.user_repo)
        self.aggregation_service = AggregationService(
            self.user_service, self.vital_service
        )

    def test_average_vitals_value_of_user(self):
        user = User("alice", 30, Gender.FEMALE, [])
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

        aggregate = self.aggregation_service.average_vitals_value_of_user(
            user.username, vital_id, timestamp1, timestamp2
        )

        self.assertEqual(aggregate, 77.5)

    def test_population_insights(self):
        user1 = User("alice", 30, Gender.FEMALE, [])
        user2 = User("bob", 35, Gender.MALE, [])
        user3 = User("charlie", 28, Gender.MALE, [])
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        vital1 = Vital(user1.username, vital_id, 75, timestamp1)
        vital2 = Vital(user2.username, vital_id, 80, timestamp2)
        self.user_service.create_user(
            user1.username, user1.age, user1.gender, user1.illness
        )
        self.user_service.create_user(
            user2.username, user2.age, user2.gender, user2.illness
        )
        self.user_service.create_user(
            user3.username, user3.age, user3.gender, user3.illness
        )
        self.vital_service.create_vital(
            user1.username, vital_id, vital1.value, vital1.timestamp
        )
        self.vital_service.create_vital(
            user2.username, vital_id, vital2.value, vital2.timestamp
        )

        percentile = self.aggregation_service.population_insights(
            user1.username, vital_id, timestamp1, timestamp2
        )

        self.assertEqual(
            percentile, 50.0
        )  # As there are only two users with equal values

    def test_average_vitals_value_of_user_no_data(self):
        user_name = "alice"
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)

        # No user or vital data exists
        with self.assertRaises(Exception) as context:
            aggregate = self.aggregation_service.average_vitals_value_of_user(
                user_name, vital_id, timestamp1, timestamp2
            )

        self.assertIsInstance(context.exception, ObjectNotFound)

    def test_population_insights_no_data(self):
        user_name = "alice"
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)

        # No user or vital data exists
        with self.assertRaises(Exception) as context:
            percentile = self.aggregation_service.population_insights(
                user_name, vital_id, timestamp1, timestamp2
            )

        self.assertIsInstance(context.exception, ObjectNotFound)

    def test_population_insights_single_user(self):
        user = User("alice", 30, Gender.FEMALE, [])
        self.user_service.create_user(
            user.username, user.age, user.gender, user.illness
        )
        vital_id = VitalId.HEART_RATE
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 11, 0)
        value = 75
        self.vital_service.create_vital(user.username, vital_id, value, timestamp1)
        self.vital_service.create_vital(user.username, vital_id, value, timestamp2)

        percentile = self.aggregation_service.population_insights(
            user.username, vital_id, timestamp1, timestamp2
        )

        self.assertEqual(percentile, 100.0)  # Only one user in the population


if __name__ == "__main__":
    unittest.main()
