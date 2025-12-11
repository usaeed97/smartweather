# routes/auth_routes.py
from flask import Blueprint, request, jsonify

from models.user_model import create_user, verify_user
from utils.auth import encode_auth_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user_id = create_user(email, password)
    if not user_id:
        return jsonify({"message": "User already exists"}), 409

    return jsonify({"message": "User created", "user_id": user_id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = verify_user(email, password)
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    token = encode_auth_token(user["_id"])
    return jsonify({"token": token}), 200
