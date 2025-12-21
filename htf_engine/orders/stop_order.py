from .order import Order

# stop price > last traded price - buy 
# stop sell < last traded price - sell 

class StopOrder(Order):
    def __init__(self, order_id: str, side: str, stop_price: float, qty: int, user_id: str, timestamp: str):
        super().__init__(order_id, side, qty, user_id, timestamp)
        self.stop_price = stop_price
