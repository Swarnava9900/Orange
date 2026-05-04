from flask import Blueprint, request, jsonify, current_app
from utils.logger import logger

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route("/transactions/new", methods=["POST", "OPTIONS"])
def add_transaction():

    if request.method == "OPTIONS":
        return jsonify({}), 200

    blockchain = current_app.blockchain  # ✅ use app instance

    data = request.get_json()

    if not data:
        return jsonify({"error": "Transaction data required"}), 400

    blockchain.add_transaction(data)

    logger.info(f"Transaction added: {data}")
    return jsonify({"message": "Transaction added"}), 201


@transaction_bp.route("/mine", methods=["GET"])
def mine_block():

    blockchain = current_app.blockchain  # ✅ use app instance

    success = blockchain.mine_pending_transactions()

    if not success:
        return jsonify({"message": "No transactions to mine"}), 400

    # 🔄 Auto-sync with network after mining
    replaced = current_app.resolve_conflicts()

    if replaced:
        return jsonify({
            "message": "Block mined, but chain was replaced by a longer valid chain"
        }), 200

    return jsonify({
        "message": "Block successfully mined and chain is authoritative"
    }), 200