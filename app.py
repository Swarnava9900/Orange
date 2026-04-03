from flask import Flask
from routes.admin_routes import admin_bp
from routes.chain_routes import chain_bp
from routes.transaction_routes import transaction_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(admin_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(chain_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(port = 5000)