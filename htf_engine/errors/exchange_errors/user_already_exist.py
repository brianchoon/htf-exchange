from .exchange_error import ExchangeError


class UserAlreadyExist(ExchangeError):
    error_code = "USER_ALREADY_EXIST"

    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__()

    def default_message(self):
        return f"User with id {self.user_id} already exist"
