from flask import Blueprint, jsonify
import services.blockchain_service as service
from utils.logger import logger

chain_bp = Blueprint("chain", __name__)

@chain_bp.route("/chain", methods=["GET"])
def get_chain():

    if service.orange is None:
        return jsonify({"error": "Blockchain not initialized"}), 400

    chain_data = [block.__dict__ for block in service.orange.chain]

    return jsonify({
        "length": len(chain_data),
        "chain": chain_data
    }), 200