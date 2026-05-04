from flask import Blueprint, jsonify, current_app
from utils.logger import logger

chain_bp = Blueprint("chain", __name__)


@chain_bp.route("/chain", methods=["GET"])
def get_chain():

    blockchain = current_app.blockchain  # ✅ single source of truth

    chain_data = [block.__dict__ for block in blockchain.chain]

    return jsonify({
        "length": len(chain_data),
        "chain": chain_data
    }), 200