import unittest
import datetime
from models.vital import Vital, VitalId
from repo.vital import VitalRepo


class TestVitalRepo(unittest.TestCase):
    def setUp(self):
        self.vital_repo = VitalRepo()

    def test_create_and_retrieve_vital(self):
        user_name = "swati"
        vital_id = VitalId.HEART_RATE
        timestamp = datetime.datetime(2023, 1, 1, 10, 0)
        value = 75
        vital = Vital(user_name, vital_id, value, timestamp)

        self.vital_repo.create(vital)
        retrieved_vital = self.vital_repo.retrieve(user_name, vital_id, timestamp)

        self.assertEqual(retrieved_vital, vital)

    def test_update_vital(self):
        user_name = "swati"
        vital_id = VitalId.HEART_RATE
        timestamp = datetime.datetime(2023, 1, 1, 10, 0)
        value = 75
        new_value = 80
        vital = Vital(user_name, vital_id, value, timestamp)

        self.vital_repo.create(vital)
        self.vital_repo.update(vital, new_value)
        updated_vital = self.vital_repo.retrieve(
            user_name=user_name, vital_id=vital_id, timestamp=timestamp
        )

        self.assertEqual(updated_vital.value, new_value)

    def test_retrieve_vital_range(self):
        user_name = "swati"
        vital_id = VitalId.HEART_RATE
        start_ts = datetime.datetime(2023, 1, 1, 9, 0)
        end_ts = datetime.datetime(2023, 1, 1, 11, 0)

        vital1 = Vital(user_name, vital_id, 75, datetime.datetime(2023, 1, 1, 10, 0))
        vital2 = Vital(user_name, vital_id, 80, datetime.datetime(2023, 1, 1, 10, 30))
        vital3 = Vital(user_name, vital_id, 85, datetime.datetime(2023, 1, 1, 11, 0))
        vital4 = Vital(user_name, vital_id, 85, datetime.datetime(2023, 1, 1, 8, 0))

        self.vital_repo.create(vital1)
        self.vital_repo.create(vital2)
        self.vital_repo.create(vital3)
        self.vital_repo.create(vital4)

        retrieved_vitals = self.vital_repo.retrieve_vital_range(
            user_name=user_name, vital_id=vital_id, start_ts=start_ts, end_ts=end_ts
        )

        self.assertEqual(set(retrieved_vitals), {vital1, vital2, vital3})


if __name__ == "__main__":
    unittest.main()
