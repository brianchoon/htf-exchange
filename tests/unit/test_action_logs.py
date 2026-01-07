import json


def test_record_register_user(exchange, u1):
    exchange.register_user(u1)
    assert len(u1.user_log._actions) == 1
    assert u1.user_log._actions[0].user_id == u1.user_id
    assert u1.user_log._actions[0].username == u1.username
    assert u1.user_log._actions[0].action == "REGISTER"
    assert u1.user_log._actions[0].user_balance == u1.cash_balance


def test_record_place_order(exchange, u1):
    exchange.register_user(u1)
    u1.place_order("Stock A", "limit", "buy", 10, 10)
    assert u1.user_log._actions[0].action == "REGISTER"
    assert u1.user_log._actions[1].action == "PLACE ORDER"
    assert u1.user_log._actions[1].username == u1.username
    assert u1.user_log._actions[1].user_id == u1.user_id
    assert u1.user_log._actions[1].order_type == "limit"
    assert u1.user_log._actions[1].side == "buy"
    assert u1.user_log._actions[1].quantity == 10
    assert u1.user_log._actions[1].price == 10
    assert u1.user_log._actions[1].instrument_id == "Stock A"


def test_record_cash_in(u1):
    u1.cash_in(100)
    assert u1.user_log._actions[0].action == "CASH IN"
    assert u1.user_log._actions[0].username == u1.username
    assert u1.user_log._actions[0].user_id == u1.user_id
    assert u1.user_log._actions[0].amount_added == 100
    assert u1.user_log._actions[0].curr_balance == u1.cash_balance


def test_record_cash_out(u1):
    u1.cash_out(100)
    assert u1.user_log._actions[0].action == "CASH OUT"
    assert u1.user_log._actions[0].username == u1.username
    assert u1.user_log._actions[0].user_id == u1.user_id
    assert u1.user_log._actions[0].amount_removed == 100
    assert u1.user_log._actions[0].curr_balance == u1.cash_balance


def test_record_cancel_order(exchange, u1):
    exchange.register_user(u1)
    oid = u1.place_order("Stock A", "limit", "buy", 10, 10)
    exchange.cancel_order(u1.user_id, "Stock A", oid)
    print(u1.user_log)

    assert u1.user_log._actions[0].action == "REGISTER"
    assert u1.user_log._actions[1].action == "PLACE ORDER"
    assert u1.user_log._actions[2].action == "CANCEL ORDER"
    assert u1.user_log._actions[2].username == u1.username
    assert u1.user_log._actions[2].user_id == u1.user_id
    assert u1.user_log._actions[2].order_id == oid
    assert u1.user_log._actions[2].instrument_id == "Stock A"


def test_record_stop_trigger(exchange, u1, u2, u3):
    exchange.register_user(u1)
    exchange.register_user(u2)
    exchange.register_user(u3)
    u1.place_order("Stock A", "stop-limit", "buy", 10, price=10, stop_price=10)

    assert u1.user_log._actions[0].action == "REGISTER"
    assert u1.user_log._actions[1].action == "PLACE ORDER"

    u2.place_order("Stock A", "limit", "buy", 10, price=10)
    u3.place_order("Stock A", "limit", "sell", 10, price=10)

    assert u1.user_log._actions[2].action == "STOP TRIGGER"
    assert u1.user_log._actions[2].username == u1.username
    assert u1.user_log._actions[2].user_id == u1.user_id
    assert u1.user_log._actions[2].instrument_id == "Stock A"
    assert u1.user_log._actions[2].underlying_order_type == "limit"
    assert u1.user_log._actions[2].order_type == "stop-limit"
    assert u1.user_log._actions[2].side == "buy"
    assert u1.user_log._actions[2].quantity == 10
    assert u1.user_log._actions[2].stop_price == 10
    assert u1.user_log._actions[2].price == 10


def test_jsonify_user_logs(exchange, u1):
    exchange.register_user(u1)
    u1.place_order("Stock A", "limit", "buy", 10, 10)
    u1.place_order("Stock B", "limit", "sell", 10, 10)
    u1.cash_in(100)
    u1.cash_out(100)
    u1.place_order("Stock C", "limit", "buy", 10, 10)

    logs = u1.user_log.get_logs_seriable()

    # A. Check total count
    assert len(logs) == 6

    # B. Verify Schema of Entry 0 (REGISTER)
    reg_log = logs[0]
    assert reg_log["action"] == "REGISTER"
    assert reg_log["user_id"] == u1.user_id
    assert reg_log["user_balance"] == 5000
    assert isinstance(
        reg_log["timestamp"], str
    )  # Verify it is a string, not datetime object

    # C. Verify Schema of Entry 1 (PLACE ORDER - BUY)
    buy_log = logs[1]
    assert buy_log["action"] == "PLACE ORDER"
    assert buy_log["instrument_id"] == "Stock A"
    assert buy_log["side"] == "buy"
    assert buy_log["quantity"] == 10
    assert buy_log["price"] == 10
    assert buy_log["stop_price"] is None  # Check null handling

    # D. Verify Schema of Entry 3 (CASH IN)
    cash_in_log = logs[3]
    assert cash_in_log["action"] == "CASH IN"
    assert cash_in_log["amount_added"] == 100
    assert cash_in_log["curr_balance"] == 5100  # 5000 start + 100

    # E. Verify Schema of Entry 4 (CASH OUT)
    cash_out_log = logs[4]
    assert cash_out_log["action"] == "CASH OUT"
    assert cash_out_log["amount_removed"] == 100
    assert cash_out_log["curr_balance"] == 5000  # Back to 5000
