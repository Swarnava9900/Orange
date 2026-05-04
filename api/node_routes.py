from flask import Blueprint, request, jsonify, current_app

node_bp = Blueprint("nodes", __name__)


# 🔹 Register new nodes
@node_bp.route("/nodes/register", methods=["POST"])
def register_nodes():
    values = request.get_json()

    if not values or "nodes" not in values:
        return jsonify({"message": "No nodes provided"}), 400

    nodes = values.get("nodes")

    for node in nodes:
        current_app.register_node(node)  # ✅ use app method

    return jsonify({
        "message": f"{len(nodes)} nodes registered",
        "nodes": current_app.get_nodes()
    }), 201

# 🔹 Check active nodes
@node_bp.route("/nodes/check", methods=["GET"])
def check_nodes():

    active = current_app.check_nodes()  # ✅ use app method

    return jsonify({
        "active_nodes": active,
        "count": len(active)
    }), 200

# 🔹 Resolve conflicts (consensus)
@node_bp.route("/nodes/resolve", methods=["GET"])
def resolve():

    replaced = current_app.resolve_conflicts()  # ✅ use app method

    if replaced:
        return jsonify({
            "message": "Chain replaced with longer valid chain"
        }), 200
    else:
        return jsonify({
            "message": "Current chain is authoritative"
        }), 200