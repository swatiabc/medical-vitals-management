"""
Purpose: To add User data into inmemory database (dictionary)
No complicated business logic is required or added here
Will be using Red Black tree to insert Vital instances in order of their timestamps
Reasons for choosing Red black tree:
 1. we need to insert elements in sorted manner (according to timestamp)
 2. we need to fetch Vital instances within a range of timestamp (using RB tree will optimize the query)

sample vital data:
{
    "user_name": {
        "HEART_RATE": rb_tree_instance,
        "TEMPERATURE": rb_tree_instance
    },
}
"""

import datetime

from models.vital import Vital, VitalId
from utils.rb_tree.execute import RedBlackExecuter


class VitalRepo:
    PRIMARY_KEY = 1

    def __init__(self) -> None:
        self.__vitals = {}
        self.rb_executor = RedBlackExecuter

    @property
    def vitals(self) -> dict:
        return self.__vitals

    def create(self, vital: Vital):
        """

        :param vital:
        :return:

        Will use the rb_tree_instance mapped with the given username and vital_id.
        If rb_tree_instance is not present, we will create one
        """
        vital.id = self.PRIMARY_KEY
        self.PRIMARY_KEY += 1

        if not self.__vitals.get(vital.user_name):
            self.__vitals[vital.user_name] = {}
        if not self.__vitals.get(vital.user_name).get(vital.vital_id):
            self.__vitals[vital.user_name][vital.vital_id] = self.rb_executor()

        rb_executor = self.__vitals[vital.user_name][vital.vital_id]
        rb_executor.insert(vital, vital.timestamp)

    def retrieve(
        self, user_name: str, vital_id: VitalId, timestamp: datetime.datetime
    ) -> Vital:
        """

        :param user_name:
        :param vital_id:
        :param timestamp:
        :return:
        we will use RBTree search function to searhc the node optimally
        """
        rb_executor = self.__vitals[user_name][vital_id]
        vital = rb_executor.search(timestamp)
        return vital

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
        Will use retrieve_for_a_period in RBTree to fetch the list optimally
        """
        rb_executor = self.__vitals[user_name][vital_id]
        vitals = rb_executor.retrieve_for_a_period(value1=start_ts, value2=end_ts)
        return vitals

    def update(self, vital: Vital, value: int) -> None:
        vital.value = value
