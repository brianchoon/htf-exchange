from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Trade:
    timestamp: datetime
    price: float
    qty: int
    buy_order_id: int
    sell_order_id: int
    aggressor: str

    def __str__(self):
        ts = self.timestamp.isoformat().replace("+00:00", "Z")
        side = self.aggressor.upper()

        return (
            f"{ts} | {side} {self.qty} @ {self.price} | "
            f"buy_oid={self.buy_order_id} sell_oid={self.sell_order_id}"
        )
