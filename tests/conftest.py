import pytest
from unittest.mock import patch
import sys
import os

from htf_engine.exchange import Exchange
from htf_engine.order_book import OrderBook
from htf_engine.user.user import User
from htf_engine.trades.trade_log import TradeLog

from ui.app import app as flask_app

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


@pytest.fixture
def ob():
    e = Exchange(fee=10)
    o = OrderBook("NVDA", enable_stp=False)

    e.add_order_book("NVDA", o)
    e.register_user(User("TESTING: NO_USER_ID", "TESTING: NO_USER_ID", 5000))

    return o


@pytest.fixture
def exchange():
    e = Exchange(fee=10)
    e.add_order_book("Stock A", OrderBook("Stock A"))
    e.add_order_book("Stock B", OrderBook("Stock B"))
    e.add_order_book("Stock C", OrderBook("Stock C"))
    return e


@pytest.fixture
def u1():
    return User("ceo_of_fumbling", "Zi Shen", 5000)


@pytest.fixture
def u2():
    return User("cheater6767", "Clemen", 5000)


@pytest.fixture
def u3():
    return User("csgod", "Brian", 5000)


@pytest.fixture
def trade_log():
    return TradeLog()


@pytest.fixture
def brian():
    """Creates a test user 'brian'."""
    return User("brian", "Brian", 1_000_000)


@pytest.fixture
def clemen():
    """Creates a test user 'clemen'."""
    return User("clemen", "Clemen", 1_000_000)


@pytest.fixture
def apple_book(exchange):
    """Creates the AAPL order book and adds it to the exchange."""
    ob = OrderBook("AAPL")
    exchange.add_order_book("AAPL", ob)
    return ob


@pytest.fixture
def client(exchange, apple_book, brian, clemen):
    """
    Creates a Flask test client with MOCKED globals.
    This is the most important part.
    """
    exchange.register_user(brian)
    exchange.register_user(clemen)

    test_users_dict = {"brian": brian, "clemen": clemen}

    with (
        patch("ui.app.exchange", exchange),
        patch("ui.app.USERS", test_users_dict),
        patch("ui.app.order_book", apple_book),
    ):
        flask_app.config["TESTING"] = True

        # Return the client so tests can make HTTP requests
        with flask_app.test_client() as client:
            yield client
