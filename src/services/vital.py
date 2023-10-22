"""
VitalService interacts with UserRepo for create and retrieve operations.
All the business logic and validation checks are present here
"""

import datetime

from exception.exception import ObjectNotFound, WrongChoice
from models.user import User
from models.vital import VitalId, Vital
from repo.user import UserRepo
from repo.vital import VitalRepo


class VitalService:
    def __init__(self, vital_repo: VitalRepo, user_repo: UserRepo) -> None:
        self.vital_repo = vital_repo
        self.user_repo = user_repo

    def create_vital(
        self,
        user_name: User.username,
        vital_id: VitalId,
        value: int,
        timestamp: datetime.datetime,
    ) -> None:
        """

        :param user_name:
        :param vital_id:
        :param value:
        :param timestamp:
        :return:
        Create Vital instance if:
         1. given vital_id belongs to VitalId
         2. Username is present in User
        """
        if not self.user_repo.retrieve(user_name):
            raise ObjectNotFound(User, user_name=user_name)
        try:
            vital_type = VitalId[vital_id]
        except KeyError:
            raise WrongChoice(VitalId, vital_id=vital_id)
        vital = Vital(
            user_name=user_name, vital_id=vital_type, value=value, timestamp=timestamp
        )
        self.vital_repo.create(vital)

    def update_vital(
        self,
        user_name: str,
        value: int,
        vital_id: VitalId,
        timestamp: datetime.datetime,
    ) -> None:
        """

        :param user_name:
        :param value:
        :param vital_id:
        :param timestamp:
        :return:
        update Vital instance if given combination of username and vitalid and timestamp exists.
        Otherwise raise exception
        """
        if not (
            self.vital_repo.vitals.get(user_name)
            and self.vital_repo.vitals.get(user_name).get(vital_id)
        ):
            raise ObjectNotFound(Vital, user_name=user_name, vital_id=vital_id)
        vital = self.vital_repo.retrieve(user_name, vital_id, timestamp)
        if not vital:
            raise ObjectNotFound(
                Vital, user_name=user_name, vital_id=vital_id, timestamp=timestamp
            )
        self.vital_repo.update(vital, value)

    def retrieve_vital_range(
        self,
        user_name: str,
        vital_id: VitalId,
        start_ts: datetime.datetime,
        end_ts: datetime.datetime,
    ) -> list:
        """

        :param user_name:
        :param vital_id:
        :param start_ts:
        :param end_ts:
        :return:
        retrieve vital instances whose timestamp falls between the given start_ts and end_ts
        """
        if not (
            self.vital_repo.vitals.get(user_name)
            and self.vital_repo.vitals.get(user_name).get(vital_id)
        ):
            raise ObjectNotFound(Vital, user_name=user_name, vital_id=vital_id)
        vitals = self.vital_repo.retrieve_vital_range(
            user_name, vital_id, start_ts, end_ts
        )
        return vitals
