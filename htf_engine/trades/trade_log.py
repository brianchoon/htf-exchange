from datetime import datetime, timezone
from .trade import Trade


class TradeLog:
    VALID_AGGRESSORS = {"buy", "sell"}

    def __init__(self):
        self.trades = []

    def record(
        self,
        price,
        qty,
        buy_order_id,
        sell_order_id,
        aggressor
    ):
        if aggressor not in self.VALID_AGGRESSORS:
            raise ValueError(f"Invalid aggressor: {aggressor}")

        trade = Trade(
            timestamp=datetime.now(timezone.utc),
            price=price,
            qty=qty,
            buy_order_id=buy_order_id,
            sell_order_id=sell_order_id,
            aggressor=aggressor,
        )
        self.trades.append(trade)
        return trade

    def retrieve_log(self):
        return list(self.trades)        # defensive copy
    