from .rejected_order_error import RejectedOrderError


class FOKInsufficientLiquidityError(RejectedOrderError):
    error_code = "FOK_INSUFFICIENT_LIQUIDITY"

    def default_message(self) -> str:
        return self.header_string() + "FOK order had insufficient liquidity and was rejected."
    