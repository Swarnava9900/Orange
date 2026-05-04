import argparse
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from api.node_routes import node_bp as nodes
from api.admin_routes import admin_bp as admin
from api.chain_routes import chain_bp as chain
from api.transaction_routes import transaction_bp as transaction

from config.db import db
from config.config import Config

from core.blockchain import Blockchain

from services import node_service


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.blockchain = Blockchain()
        app.nodes = set()
        app.admin_password_hash = None

    CORS(app, resources={r"/*": {"origins": "*"}})

    JWTManager(app)

    # -------------------------------
    # 🔗 Attach node service methods
    # -------------------------------
    app.register_node = lambda address: node_service.register_node(app, address)
    app.get_nodes = lambda: node_service.get_nodes(app)
    app.check_nodes = lambda: node_service.check_nodes(app)
    app.resolve_conflicts = lambda: node_service.resolve_conflicts(app)

    # -------------------------------
    # 🔌 Register API routes
    # -------------------------------
    app.register_blueprint(admin)
    app.register_blueprint(transaction)
    app.register_blueprint(chain)
    app.register_blueprint(nodes)

    return app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug=True)