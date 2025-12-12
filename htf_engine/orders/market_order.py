from .order import Order


class MarketOrder(Order):
    def __init__(self, order_id, side, qty):
        super().__init__(order_id, side, qty)

    def __str__(self):
        return f"[ID {self.order_id}] {self.side.upper()} any x {self.qty}"