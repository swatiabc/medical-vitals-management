import json

from enum import Enum

from repo.user import UserRepo
from repo.vital import VitalRepo
from services.aggregation import AggregationService
from services.user import UserService
from services.vital import VitalService
from view.aggregate import AggregateView
from view.user import UserView
from view.vital import VitalView


class Command(str, Enum):
    create_user = "create_user"
    insert_vital = "insert_vital"
    aggregate = "aggregate"
    population_insight = "population_insight"
    get_vitals = "get_vitals"
    delete_vitals = "delete_vitals"
    get_user = "get_user"
    update_vital = "update_vital"


if __name__ == "__main__":
    with open("test_case.json", "r") as json_file:
        data_list = json.load(json_file)

    user_repo = UserRepo()
    user_service = UserService(user_repo)
    vital_repo = VitalRepo()
    vital_service = VitalService(vital_repo, user_repo)
    aggregate_service = AggregationService(user_service, vital_service)
    user_view = UserView(user_service)
    aggregate_view = AggregateView(user_service, vital_service, aggregate_service)
    vital_view = VitalView(user_service, vital_service)

    for data in data_list:
        command = data.get("command")
        if command == Command.get_user.value:
            response = user_view.get_user(data)
            print(response)
        elif command == Command.aggregate.value:
            response = aggregate_view.aggregate(data)
            print(response)
        elif command == Command.create_user.value:
            response = user_view.create_user(data)
            print(response)
        elif command == Command.insert_vital.value:
            response = vital_view.insert_vital(data)
            print(response)
        elif command == Command.get_vitals.value:
            response = vital_view.get_vitals(data)
            print(response)
        elif command == Command.population_insight.value:
            response = aggregate_view.population_insight(data)
            print(response)
        elif command == Command.update_vital.value:
            response = vital_view.update_vital(data)
            print(response)
        else:
            print("Invalid command type: ", command)
