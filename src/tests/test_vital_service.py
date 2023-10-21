import unittest
import datetime
from models.user import User
from models.vital import VitalId, Vital
from repo.user import UserRepo
from repo.vital import VitalRepo
from services.vital import VitalService


class TestVitalService(unittest.TestCase):
    def setUp(self):
        self.user_repo = UserRepo()
        self.vital_repo = VitalRepo()
        self.vital_service = VitalService(self.vital_repo, self.user_repo)

        # Create a user for testing
        self.user = User("swati", 30, "FEMALE", [])

    def test_create_and_retrieve_vital(self):
        user_name = "swati"
        vital_id = VitalId.HEART_RATE
        timestamp = datetime.datetime(2023, 1, 1, 10, 0)
        value = 75

        self.user_repo.create(self.user)
        self.vital_service.create_vital(user_name, vital_id, value, timestamp)
        retrieved_vitals = self.vital_service.retrieve_vital_range(
            user_name, vital_id, timestamp, timestamp
        )
        retrieved_values = [v.value for v in retrieved_vitals]
        self.assertEqual(retrieved_values, [value])

    def test_update_vital(self):
        user_name = "swati"
        vital_id = VitalId.HEART_RATE
        timestamp = datetime.datetime(2023, 1, 1, 10, 0)
        value = 75
        new_value = 80

        self.user_repo.create(self.user)
        self.vital_service.create_vital(user_name, vital_id, value, timestamp)
        self.vital_service.update_vital(user_name, new_value, vital_id, timestamp)
        retrieved_vitals = self.vital_service.retrieve_vital_range(
            user_name, vital_id, timestamp, timestamp
        )
        retrieved_values = [v.value for v in retrieved_vitals]

        self.assertEqual(retrieved_values, [new_value])

    def test_retrieve_vital_range(self):
        user_name = "swati"
        vital_id = VitalId.HEART_RATE
        start_ts = datetime.datetime(2023, 1, 1, 9, 0)
        end_ts = datetime.datetime(2023, 1, 1, 11, 0)
        timestamp1 = datetime.datetime(2023, 1, 1, 10, 0)
        timestamp2 = datetime.datetime(2023, 1, 1, 10, 30)
        timestamp3 = datetime.datetime(2023, 1, 1, 11, 0)

        self.user_repo.create(self.user)
        self.vital_service.create_vital(user_name, vital_id, 75, timestamp1)
        self.vital_service.create_vital(user_name, vital_id, 80, timestamp2)
        self.vital_service.create_vital(user_name, vital_id, 85, timestamp3)
        retrieved_vitals = self.vital_service.retrieve_vital_range(
            user_name, vital_id, start_ts, end_ts
        )
        retrieved_values = [v.value for v in retrieved_vitals]

        self.assertEqual(set(retrieved_values), {75, 80, 85})


if __name__ == "__main__":
    unittest.main()
