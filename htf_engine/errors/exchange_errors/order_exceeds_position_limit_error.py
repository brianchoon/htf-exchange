from .rejected_order_error import RejectedOrderError


class OrderExceedsPositionLimitError(RejectedOrderError):
    error_code = "ORDER_EXCEEDS_POSITION_LIMIT"

    def __init__(self, inst: str, side: str, qty: int, quota: dict[str, int]):
        self.inst = inst
        self.side = side
        self.qty = qty
        self.quota = quota
        super().__init__()

    def default_message(self) -> str:
        return (
            self.header_string()
            + f"Cannot place {self.side} order for {self.qty}x {self.inst} as it exceeds the quota of {self.quota[f'{self.side}_quota']}."
        )
