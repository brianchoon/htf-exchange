import json


def test_place_order_route(client, brian):
    """
    Test that calling POST /place_order actually modifies
    the engine state for user 'brian'.
    """

    payload = {
        "user_id": "brian",
        "instrument": "AAPL",
        "order_type": "limit",
        "side": "buy",
        "qty": 10,
        "price": 150.0,
        "stop_price": "",
    }

    response = client.post("/place_order", json=payload)

    assert response.status_code == 200
    data = response.json
    assert data["status"] == "ok"
    assert "order_id" in data
    assert brian.cash_balance == 1000000
    assert brian.outstanding_buys["AAPL"] == 10


def test_place_stop_order_route(client, brian):
    """
    Test the calling POST for place stop order
    """
    payload = {
        "user_id": "brian",
        "instrument": "AAPL",
        "order_type": "stop-limit",
        "side": "buy",
        "qty": 10,
        "price": 150.0,
        "stop_price": 140.0,
    }

    response = client.post("/place_order", json=payload)

    assert response.status_code == 200
    data = response.json
    assert data["status"] == "ok"
    assert "order_id" in data
    assert brian.cash_balance == 1000000
    assert brian.outstanding_buys["AAPL"] == 10
    assert brian.user_log._actions[1].action == "PLACE ORDER"
    assert brian.user_log._actions[1].order_type == "stop-limit"
    assert brian.user_log._actions[1].stop_price == 140.0


def test_modify_order_route(client, brian):
    """
    Test the calling POST for modify order
    """
    order = {
        "user_id": "brian",
        "instrument": "AAPL",
        "order_type": "limit",
        "side": "buy",
        "qty": 10,
        "price": 150.0,
        "stop_price": "",
    }

    response = client.post("/place_order", json=order)
    assert response.status_code == 200
    data = response.json
    assert data["status"] == "ok"
    assert "order_id" in data

    order_id = data["order_id"]

    modification = {
        "user_id": "brian",
        "order_id": order_id,
        "instrument": "AAPL",
        "new_qty": 5,
        "new_price": 150.0,
    }

    response2 = client.post("/modify_order", json=modification)
    assert response2.status_code == 200
    data2 = response2.json
    assert data2["status"] == "ok"
    assert "new_oid" in data2
    assert brian.outstanding_buys["AAPL"] == 5
    assert brian.user_log._actions[2].action == "MODIFY ORDER"
    assert brian.user_log._actions[2].new_qty == 5


def test_cancel_order(client, brian):
    """
    Test the calling POST for cancel order
    """
    order = {
        "user_id": "brian",
        "instrument": "AAPL",
        "order_type": "limit",
        "side": "buy",
        "qty": 10,
        "price": 150.0,
        "stop_price": "",
    }

    response = client.post("/place_order", json=order)
    assert response.status_code == 200
    data = response.json
    assert data["status"] == "ok"
    assert "order_id" in data

    order_id = data["order_id"]

    cancellation = {"user_id": "brian", "order_id": order_id, "instrument": "AAPL"}

    response2 = client.post("/cancel_order", json=cancellation)
    assert response2.status_code == 200
    data2 = response2.json
    assert data2["status"] == "ok"
    assert brian.outstanding_buys["AAPL"] == 0
    assert brian.user_log._actions[2].action == "CANCEL ORDER"


def test_user_positions(client, brian, clemen, exchange):
    """
    Test /positions/<user_id> endpoint
    """
    order = {
        "user_id": "brian",
        "instrument": "AAPL",
        "order_type": "limit",
        "side": "buy",
        "qty": 10,
        "price": 150.0,
        "stop_price": "",
    }
    response = client.post("/place_order", json=order)

    order2 = {
        "user_id": "clemen",
        "instrument": "AAPL",
        "order_type": "limit",
        "side": "sell",
        "qty": 10,
        "price": 150.0,
        "stop_price": "",
    }
    response2 = client.post("/place_order", json=order2)
    assert response.status_code == 200
    assert response2.status_code == 200

    response = client.get(f"/positions/{brian.user_id}")
    assert response.status_code == 200
    data = response.json
    assert data["positions"] == {"AAPL": {"quantity": 10, "average_cost": 150.0}}
    assert data["outstanding_sells"] == {}
    assert data["realised_pnl"] == 0
    assert data["unrealised_pnl"] == 0


def test_register_new_user(client, exchange):
    """
    Test that /register_user adds a user to both the
    global USERS dict and the Exchange engine.
    """
    payload = {"user_id": "new_guy", "username": "NewGuy", "balance": 500}

    response = client.post("/register_user", json=payload)
    assert response.status_code == 200

    # Verify he exists in the exchange engine
    assert "new_guy" in exchange.users
    assert exchange.users["new_guy"].cash_balance == 500


def test_get_user_logs(exchange, client, brian):
    order = {
        "user_id": "brian",
        "instrument": "AAPL",
        "order_type": "limit",
        "side": "buy",
        "qty": 10,
        "price": 150.0,
        "stop_price": "",
    }
    response = client.post("/place_order", json=order)
    assert response.status_code == 200

    response = client.get(f"/action_log/{brian.user_id}")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert data[0]["action"] == "REGISTER"
    assert data[1]["action"] == "PLACE ORDER"
