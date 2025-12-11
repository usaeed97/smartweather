# app.py
import os
from flask import Flask, jsonify
from config import Config
from models.db import init_db
from routes.auth_routes import auth_bp
from routes.weather_routes import weather_bp
from routes.notes_routes import notes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init DB
    init_db(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(weather_bp, url_prefix="/api")
    app.register_blueprint(notes_bp, url_prefix="/api")

    # Simple health check
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
