from flask import Blueprint, current_app, jsonify, request

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "Customer Accounts"}), 200


@accounts_bp.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json(silent=True) or {}
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    accounts = current_app.config["ACCOUNTS"]
    account_id = str(max([int(key) for key in accounts] or [0]) + 1)
    account = {
        "id": account_id,
        "name": data["name"],
        "email": data["email"],
    }
    accounts[account_id] = account
    return jsonify(account), 201


@accounts_bp.route("/accounts", methods=["GET"])
def list_accounts():
    return jsonify(list(current_app.config["ACCOUNTS"].values())), 200


@accounts_bp.route("/accounts/<account_id>", methods=["GET"])
def read_account(account_id):
    account = current_app.config["ACCOUNTS"].get(account_id)
    if account is None:
        return jsonify({"error": "account not found"}), 404
    return jsonify(account), 200


@accounts_bp.route("/accounts/<account_id>", methods=["PUT"])
def update_account(account_id):
    accounts = current_app.config["ACCOUNTS"]
    account = accounts.get(account_id)
    if account is None:
        return jsonify({"error": "account not found"}), 404

    data = request.get_json(silent=True) or {}
    for key in ("name", "email"):
        if key in data:
            account[key] = data[key]

    return jsonify(account), 200


@accounts_bp.route("/accounts/<account_id>", methods=["DELETE"])
def delete_account(account_id):
    accounts = current_app.config["ACCOUNTS"]
    if account_id not in accounts:
        return jsonify({"error": "account not found"}), 404

    del accounts[account_id]
    return "", 204