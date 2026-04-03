from flask import Blueprint, request, jsonify
from blockchain.blockchain import Blockchain
from services.auth_service import hash_password, verify_password
import services.blockchain_service as service
from utils.logger import logger

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin-orange-start", methods=["POST"])
def start_orange():

    data = request.get_json()

    if not data or "pwd" not in data:
        return jsonify({"error": "Password required"}), 400

    service.orange = Blockchain()
    service.admin_password_hash = hash_password(data["pwd"])
    
    logger.info("Genesis block created")
    return jsonify({"message": "Genesis block created"}), 201


@admin_bp.route("/admin-orange-del", methods=["POST"])
def delete_orange():

    data = request.get_json()

    if not data or "pwd" not in data:
        logger.warning("Password required to delete blockchain")
        return jsonify({"error": "Password required"}), 400

    if service.orange is None:
        logger.info("Blockchain not initialized")
        return jsonify({"error": "Blockchain not initialized"}), 400

    if verify_password(data["pwd"], service.admin_password_hash):
        service.orange.clear_chain()
        return jsonify({"message": "Successfully deleted Orange Blockchain"}), 200

    logger.warning("Unauthorized blockchain delete attempt")
    return jsonify({"error": "Unauthorized operation"}), 403