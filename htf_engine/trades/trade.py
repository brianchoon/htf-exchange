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
