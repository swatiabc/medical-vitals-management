class ObjectNotFound(Exception):
    def __init__(self, model_name, **kwargs):
        super().__init__(f"{model_name} with kwargs {kwargs} does not exist")


class DuplicateObject(Exception):
    def __init__(self, model_name, **kwargs):
        super().__init__(f"{model_name} already exists with kwargs {kwargs}")


class WrongChoice(Exception):
    def __init__(self, class_name, **kwargs):
        super().__init__(f"{kwargs} not found in {class_name}")


class ValidationError(Exception):
    def __init__(self, data):
        super().__init__(data)
