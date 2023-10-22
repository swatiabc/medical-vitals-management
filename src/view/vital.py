"""
VitalView: directly interacts with main.py
"""

import datetime

from exception.exception import ObjectNotFound, WrongChoice
from models.vital import VitalId
from services.user import UserService
from services.vital import VitalService


class VitalView:
    def __init__(self, user_service: UserService, vital_service: VitalService):
        self.user_service = user_service
        self.vital_service = vital_service

    def insert_vital(self, command: dict) -> dict:
        """
        creates a new vital for a user, using the information in the command
        :param command: {
            "command": "insert_vital",
            "username": "Alice",
            "vital_id": "HEART_RATE",
            "value": 75,
            "timestamp": "2023-10-01 12:30:00"
        }
        :return:
        """
        username = command.get("username")
        vital_id = command.get("vital_id")
        value = command.get("value")
        timestamp = datetime.datetime.strptime(
            command.get("timestamp"), "%Y-%m-%d %H:%M:%S"
        )
        try:
            vital_type = VitalId[vital_id]
        except KeyError:
            raise WrongChoice(VitalId, vital_id=vital_id)

        self.vital_service.create_vital(username, vital_type, value, timestamp)

        return {
            "status": "success",
            "message": f"Vital {vital_id} for {username} inserted successfully.",
        }

    def get_vitals(self, command: dict) -> dict:
        """
                retrieves a particular vital usinf the information provided in the command
                :param command: {
          "command": "get_vitals",
          "username": "Alice",
          "period": ["2020-10-04", "2024-10-05"]
        }
                :return:
        """
        username = command.get("username")
        period = command.get("period")
        start_date = datetime.datetime.strptime(period[0], "%Y-%m-%d %H:%M:%S")

        end_date = datetime.datetime.strptime(period[1], "%Y-%m-%d %H:%M:%S")
        data_list = []

        for v in VitalId:
            try:
                vitals = self.vital_service.retrieve_vital_range(
                    username, v, start_date, end_date
                )
                for vital in vitals:
                    data = {
                        "vital_id": vital.vital_id.value,
                        "value": vital.value,
                        "timestamp": vital.timestamp,
                    }
                    data_list.append(data)
            except ObjectNotFound:
                continue

        return {"status": "success", "data": data_list}

    def update_vital(self, command: dict) -> dict:
        """

        :param command: {
            "command": "update_vital",
            "username": "Alice",
            "vital_id": "HEART_RATE",
            "timestamp": "2023-10-03 14:30:00",
            "value": 89
        }
        :return:
        """
        username = command.get("username")
        vital_id = command.get("vital_id")
        timestamp = datetime.datetime.strptime(
            command.get("timestamp"), "%Y-%m-%d %H:%M:%S"
        )
        value = command.get("value")

        try:
            vital_type = VitalId[vital_id]
        except KeyError:
            raise WrongChoice(VitalId, vital_id=vital_id)

        self.vital_service.update_vital(username, value, vital_type, timestamp)
        return {
            "status": "success",
            "message": f"{vital_id} was successfully updated for {username}",
        }
