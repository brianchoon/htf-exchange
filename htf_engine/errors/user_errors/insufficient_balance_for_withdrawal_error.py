from .user_error import UserError


class InsufficientBalanceForWithdrawalError(UserError):
    error_code = "INSUFFICIENT_BALANCE_FOR_WITHDRAWAL"

    def __init__(self, withdrawal_amt: float, user_cash_balance: float):
        self.withdrawal_amt = withdrawal_amt
        self.user_cash_balance = user_cash_balance
        super().__init__()

    def default_message(self) -> str:
        return f"Unable to withdraw ${self.withdrawal_amt} as user only has ${self.user_cash_balance}."
