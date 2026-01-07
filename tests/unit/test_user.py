def test_register_user(exchange, u1):
    exchange.register_user(u1)
    assert u1.user_id in exchange.users
    assert exchange.users[u1.user_id] == u1
    assert u1.place_order_callback is not None
    assert u1.user_log is not None


def test_cash_in(u1):
    u1.cash_in(100)
    assert u1.cash_balance == 5100


def test_cash_out(u1):
    u1.cash_out(50)
    assert u1.cash_balance == 4950


def test_place_buy_order(exchange, u1):
    exchange.register_user(u1)
    u1.place_order("Stock A", "limit", "buy", 10, 10)
    assert u1.outstanding_buys["Stock A"] == 10
    assert u1.outstanding_sells["Stock A"] == 0
    assert u1.cash_balance == 5000


def test_place_sell_order(exchange, u1):
    exchange.register_user(u1)
    u1.place_order("Stock A", "limit", "sell", 10, 10)
    assert u1.outstanding_buys["Stock A"] == 0
    assert u1.outstanding_sells["Stock A"] == 10
    assert u1.cash_balance == 5000
