from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required

from services.auth_service import hash_password, verify_password
from utils.logger import logger


admin_bp = Blueprint("admin", __name__)


# 🔹 Initialize blockchain (ONLY sets admin password now)
@admin_bp.route("/admin/orange/start", methods=["POST"])
def start_orange():

    blockchain = current_app.blockchain

    # ✅ Already initialized check
    if len(blockchain.chain) > 1:
        return jsonify({"error": "Blockchain already initialized"}), 400

    data = request.get_json()

    if not data or "pwd" not in data:
        return jsonify({"error": "Password required"}), 400

    # 🔐 Store admin password in app
    current_app.admin_password_hash = hash_password(data["pwd"])

    logger.info("Blockchain initialized successfully")
    return jsonify({"message": "Blockchain ready"}), 201


# 🔹 Admin login
@admin_bp.route("/admin/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "pwd" not in data:
        return jsonify({"error": "Password required"}), 400

    if not hasattr(current_app, "admin_password_hash"):
        return jsonify({"error": "Admin not initialized"}), 400

    if verify_password(data["pwd"], current_app.admin_password_hash):
        token = create_access_token(identity="admin")
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid password"}), 401


# 🔹 Delete blockchain (reset to genesis)
@admin_bp.route("/admin/orange/del", methods=["POST"])
@jwt_required()
def delete_orange():

    blockchain = current_app.blockchain

    data = request.get_json()

    if not data or "pwd" not in data:
        logger.warning("Password required to delete blockchain")
        return jsonify({"error": "Password required"}), 400

    if not hasattr(current_app, "admin_password_hash"):
        return jsonify({"error": "Admin not initialized"}), 400

    if verify_password(data["pwd"], current_app.admin_password_hash):
        blockchain.clear_chain()
        logger.warning("Orange Blockchain deleted.")
        return jsonify({"message": "Successfully deleted Orange Blockchain"}), 200

    logger.warning("Unauthorized blockchain delete attempt")
    return jsonify({"error": "Unauthorized operation"}), 403