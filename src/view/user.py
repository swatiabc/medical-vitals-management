"""
UserView: interacts directly with main to create or fetch users
"""

from services.user import UserService


class UserView:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def get_user(self, command: dict) -> dict:
        """
        retrieves user from a given username
        :param command:  {
            "command": "get_user",
            "username": "Alice"
        }
        :return:
        """
        username = command.get("username")
        user = self.user_service.retrieve_user(username)
        return {
            "status": "success",
            "data": {
                "user_name": user.username,
                "age": user.age,
                "gender": user.gender,
                "illness": user.illness,
            },
            "message": f"{username} fetched successfully",
        }

    def create_user(self, command: dict) -> dict:
        """
        creates user from the information provided in the command
        :param command: {
            "command": "create_user",
            "username": "Alice",
            "age": 25,
            "gender": "Female"
        }
        :return:
        """
        username = command.get("username")
        age = command.get("age")
        gender = command.get("gender")
        illness = command.get("illness")
        self.user_service.create_user(username, age, gender, illness)
        return {
            "status": "success",
            "message": f"User {username} created successfully.",
        }
