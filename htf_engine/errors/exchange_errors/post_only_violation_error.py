from .rejected_order_error import RejectedOrderError


class PostOnlyViolationError(RejectedOrderError):
    error_code = "POST_ONLY_VIOLATION"

    def default_message(self) -> str:
        return (
            self.header_string()
            + "Post-only order would take liquidity and was rejected."
        )
