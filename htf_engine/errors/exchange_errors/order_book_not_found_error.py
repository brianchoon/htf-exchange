from .exchange_error import ExchangeError


class OrderBookNotFoundError(ExchangeError):
    error_code = "ORDER_BOOK_NOT_FOUND"

    def __init__(self, inst: str):
        self.inst = inst
        super().__init__()

    def default_message(self) -> str:
        return f"Order Book for instrument '{self.inst}' is not registered with the exchange."
