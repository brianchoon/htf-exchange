def test_record_register_user(exchange, u1):
    exchange.register_user(u1)
    assert len(u1.user_log.actions) == 1
    assert u1.user_log.actions[0].user_id == u1.user_id
    assert u1.user_log.actions[0].username == u1.username
    assert u1.user_log.actions[0].action == "REGISTER"
    assert u1.user_log.actions[0].user_balance == u1.cash_balance



