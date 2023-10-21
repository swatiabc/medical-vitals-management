"""
Aggregation Serive is responsible for aggregate and insights operation.
"""

import datetime

from exception.exception import ValidationError, ObjectNotFound
from models.vital import VitalId
from services.user import UserService
from services.vital import VitalService
from utils.maths import Math


class AggregationService:
    def __init__(self, user_service: UserService, vital_service: VitalService):
        self.user_service = user_service
        self.vital_service = vital_service

    def average_vitals_value_of_user(
        self,
        user_name: str,
        vital_id: VitalId,
        start_ts: datetime.datetime,
        end_ts: datetime.datetime,
    ):
        """

        :param user_name:
        :param vital_id:
        :param start_ts:
        :param end_ts:
        :return:
        average value = sum of all the values/ number of values
        List of Vital instances will be fetched from retrieve_vital_range in vital_services.
        RBTree is used to optimally fetch this list
        """
        vital_list = self.vital_service.retrieve_vital_range(
            user_name=user_name, vital_id=vital_id, start_ts=start_ts, end_ts=end_ts
        )
        if len(vital_list) == 0:
            raise ValidationError(
                f"vital id not present for vital id: {vital_id} and timestamp {start_ts} - {end_ts}"
            )
        values = [v.value for v in vital_list]
        aggregate = Math.average(values)
        return aggregate

    def population_insights(
        self,
        user_name: str,
        vital_id: VitalId,
        start_ts: datetime.datetime,
        end_ts: datetime.datetime,
    ):
        """

        :param user_name:
        :param vital_id:
        :param start_ts:
        :param end_ts:
        :return: percentile of the given user for a given vital id
        """
        user_average = self.average_vitals_value_of_user(
            user_name, vital_id, start_ts, end_ts
        )

        users = self.vital_service.vital_repo.vitals
        all_averages = []
        for user in users:
            try:
                value = self.average_vitals_value_of_user(user, vital_id, start_ts, end_ts)
            except ObjectNotFound:
                continue
            all_averages.append(value)
        percentile = Math.percentile(all_averages, user_average)
        return percentile
