from flask import Blueprint, request, jsonify
import services.blockchain_service as service
from utils.logger import logger

transaction_bp = Blueprint("transactions", __name__)

@transaction_bp.route("/add-transaction", methods=["POST"])
def add_transaction():

    if service.orange is None:
        return jsonify({"error": "Blockchain not initialized"}), 400

    data = request.get_json()

    if not data:
        return jsonify({"error": "Transaction data required"}), 400

    service.orange.add_block(data)

    logger.info(f"Transaction added: {data}")
    return jsonify({"message": "Transaction added"}), 201