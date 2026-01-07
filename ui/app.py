import os
import sys

# allow importing htf-engine
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from htf_engine.exchange import Exchange
from htf_engine.user.user import User
from htf_engine.order_book import OrderBook

app = Flask(__name__)
CORS(app)

# ------------------------
# BOOTSTRAP ENGINE
# ------------------------

exchange = Exchange()

INSTRUMENT = "AAPL"

order_book = OrderBook(instrument=INSTRUMENT)
exchange.add_order_book(INSTRUMENT, order_book)

# Create user instances with name, display name, and initial balance
brian = User("brian", "Brian", 1_000_000)
clemen = User("clemen", "Clemen", 1_000_000)
charles = User("charles", "Charles", 1_000_000)
nuowen = User("nuowen", "Nuowen", 1_000_000)
zishen = User("zishen", "Zishen", 1_000_000)

# Register users with exchange
exchange.register_user(brian)
exchange.register_user(clemen)
exchange.register_user(charles)
exchange.register_user(nuowen)
exchange.register_user(zishen)

# Dictionary of users for easy access
USERS = {
    "brian": brian,
    "clemen": clemen,
    "charles": charles,
    "nuowen": nuowen,
    "zishen": zishen,
}

# ------------------------
# ROUTES
# ------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    data = request.json
    if data is None:
        return jsonify({"error": "No JSON body provided"}), 400

    if "user_id" not in data or "username" not in data or "balance" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user_id = data["user_id"]
    username = data["username"]
    balance = data["balance"]

    user = User(user_id=user_id, username=username, cash_balance=balance)
    try:
        exchange.register_user(user)
        USERS[username] = user
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON body provided"}), 400

    if (
        "user_id" not in data
        or "instrument" not in data
        or "order_type" not in data
        or "side" not in data
        or "qty" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    user_id = data["user_id"]
    instrument = data["instrument"]
    order_type = data["order_type"]  # limit/match/ioc/fok/post only/stop
    side = data["side"]  # buy / sell
    qty = int(data["qty"])
    price = data.get("price")
    stop_price = data.get("stop_price")

    if price != "":
        price = float(price)

    if stop_price != "":
        stop_price = float(stop_price)

    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "Unknown user"}), 400

    try:
        order_id = user.place_order(
            instrument=instrument,
            order_type=order_type,
            side=side,
            qty=qty,
            price=(price if order_type != "market" else None),
            stop_price=(
                stop_price if order_type in {"stop-limit", "stop-market"} else None
            ),
        )

        return jsonify({"status": "ok", "order_id": order_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/cancel_order", methods=["POST"])
def cancel_order():
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON body provided"}), 400

    if "user_id" not in data or "order_id" not in data or "instrument" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user_id = data["user_id"]
    order_id = data["order_id"]
    intrument = data["instrument"]

    try:
        exchange.cancel_order(user_id=user_id, order_id=order_id, instrument=intrument)
        return jsonify({"status": "ok"})

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400


@app.route("/modify_order", methods=["POST"])
def modify_order():
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON body provided"}), 400

    if (
        "user_id" not in data
        or "order_id" not in data
        or "instrument" not in data
        or "new_qty" not in data
        or "new_price" not in data
    ):
        return jsonify({"error": "Missing required fields"}), 400

    user_id = data["user_id"]
    order_id = data["order_id"]
    instrument = data["instrument"]
    new_qty = data["new_qty"]
    new_price = data["new_price"]

    try:
        new_oid = exchange.modify_order(
            user_id=user_id,
            order_id=order_id,
            instrument=instrument,
            new_qty=new_qty,
            new_price=new_price,
        )
        return jsonify({"status": "ok", "new_oid": new_oid})

    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400


@app.route("/positions/<user_id>")
def positions(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "Unknown user"}), 400

    return jsonify(
        {
            "positions": user.get_positions(),
            "outstanding_buys": dict(user.get_outstanding_buys()),
            "outstanding_sells": dict(user.get_outstanding_sells()),
            "realised_pnl": user.get_realised_pnl(),
            "unrealised_pnl": exchange.get_user_unrealised_pnl(user.user_id),
        }
    )


@app.route("/action_log/<user_id>")
def action_log(user_id):
    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "Unknown user"}), 400

    try:
        return jsonify(user.user_log.get_logs_seriable())
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400


@app.route("/exchange/data", methods=["POST"])
def exchange_data():
    data = request.json

    if data is None:
        return jsonify({"error": "No JSON body provided"}), 400

    if "user_id" not in data or "instrument" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user_id = data["user_id"]
    instrument = data["instrument"]
    depth = data["depth"]

    if depth != "":
        depth = int(depth)

    try:
        return jsonify(
            exchange.get_L1_data(user_id=user_id, inst=instrument, depth=depth)
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/book")
def book():
    try:
        return jsonify(order_book.snapshot())
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
