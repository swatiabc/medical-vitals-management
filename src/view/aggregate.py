"""
Service to calculate aggregate and percentile of a user's health
"""

import datetime

from exception.exception import ValidationError, WrongChoice
from models.vital import VitalId
from services.aggregation import AggregationService
from services.user import UserService
from services.vital import VitalService


class AggregateView:
    def __init__(
        self,
        user_service: UserService,
        vital_service: VitalService,
        aggregate_service: AggregationService,
    ):
        self.user_service = user_service
        self.vital_service = vital_service
        self.aggregate_service = aggregate_service

    def aggregate(self, command):
        """
        :param command:
        :return: average of values for a user's vital_id between a given timeframe
        """
        username = command.get("username")
        vital_ids = command.get("vital_ids")
        start_ts = datetime.datetime.strptime(
            command.get("start_timestamp"), "%Y-%m-%d %H:%M:%S"
        )
        end_ts = datetime.datetime.strptime(
            command.get("end_timestamp"), "%Y-%m-%d %H:%M:%S"
        )
        aggregates = {}

        for vital_id in vital_ids:
            try:
                vital_type = VitalId[vital_id]
            except KeyError:
                raise WrongChoice(VitalId, vital_id=vital_id)
            average = self.aggregate_service.average_vitals_value_of_user(
                username, vital_type, start_ts, end_ts
            )
            aggregates[vital_id] = average

        return {
            "status": "success",
            "message": "Aggregate fetched successfully.",
            "data": {
                "username": "Alice",
                "aggregates": aggregates,
                "start_timestamp": command.get("start_timestamp"),
                "end_timestamp": command.get("start_timestamp"),
            },
        }

    def population_insight(self, command):
        """

        :param command:
        :return: get percentile of a user for a vital id between a given timeframe
        """
        username = command.get("username")
        vital_type = command.get("vital_id")
        start_ts = datetime.datetime.strptime(
            command.get("start_timestamp"), "%Y-%m-%d %H:%M:%S"
        )
        end_ts = datetime.datetime.strptime(
            command.get("end_timestamp"), "%Y-%m-%d %H:%M:%S"
        )

        try:
            vital_id = VitalId[vital_type]
        except KeyError:
            raise WrongChoice(VitalId, vital_id=vital_type)

        percentile = self.aggregate_service.population_insights(
            username, vital_id, start_ts, end_ts
        )
        return {
            "status": "success",
            "message": "Population insight fetched successfully.",
            "data": {
                "username": username,
                "vital_id": vital_type,
                "start_timestamp": command.get("start_timestamp"),
                "end_timestamp": command.get("end_timestamp"),
                "insight": f"Your HeartRate is in the {percentile} percentile.",
            },
        }
