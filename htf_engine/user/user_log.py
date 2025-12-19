from datetime import datetime
from typing import List

from htf_engine.user.actionslogs.user_action import UserAction
from htf_engine.user.actionslogs.register_user_action  import RegisterUserAction
from htf_engine.user.actionslogs.cash_in_action import CashInAction
from htf_engine.user.actionslogs.cash_out_action import CashOutAction
from htf_engine.user.actionslogs.cancel_order_action import CancelOrderAction
from htf_engine.user.actionslogs.place_order_action import PlaceOrderAction

class UserLog:
    def __init__(self):
        self.actions: List[UserAction] = []

    def _get_now(self) -> datetime:
        return datetime.now()

    def record_register_user(self, user_id: int, username: str, user_balance: float):
        action = RegisterUserAction(
            timestamp=self._get_now(),
            user_id=user_id,
            username=username,
            action="REGISTER",
            user_balance=user_balance
        )
        self.actions.append(action)

    def record_place_order(self, user_id: int, username: str, instrument_id: str, order_type: str, side: str, quantity: int, price: float):
        action = PlaceOrderAction(
            timestamp=self._get_now(),
            user_id=user_id,
            username=username,
            action="PLACE ORDER",
            instrument_id=instrument_id,
            order_type=order_type,
            side=side,
            quantity=quantity,
            price=price
        )


    def record_cash_in(self, user_id: int, username: str, amount: float, new_balance: float):
        action = CashInAction(
            timestamp=self._get_now(),
            user_id=user_id,
            username=username,
            action="CASH_IN",
            amount_added=amount,
            curr_balance=new_balance
        )
        self.actions.append(action)

    def record_cash_out(self, user_id: int, username: str, amount: float, new_balance: float):
        action = CashOutAction(
            timestamp=self._get_now(),
            user_id=user_id,
            username=username,
            action="CASH_OUT",
            amount_removed=amount,
            curr_balance=new_balance
        )
        self.actions.append(action)

    def record_cancel_order(self, user_id: int, username: str, order_id: str, instrument_id: str):
        action = CancelOrderAction(
            timestamp=self._get_now(),
            user_id=user_id,
            username=username,
            action="CANCEL_ORDER",
            order_id=order_id,
            instrument_id=instrument_id
        )
        self.actions.append(action)



    def __str__(self):
        """Prints the entire audit trail."""
        return "\n".join(str(action) for action in self.actions)