from .rejected_order_error import RejectedOrderError


class SelfTradePreventionError(RejectedOrderError):
    error_code = "SELF_TRADE_PREVENTION"

    def __init__(self, order_id: str, user_id: str):
        self.order_id = order_id
        self.user_id = user_id
        super().__init__()

    def default_message(self) -> str:
        return self.header_string() + f"STP triggered: cancelling order {self.order_id} from User {self.user_id}"
    