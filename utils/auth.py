# utils/auth.py
import datetime
from functools import wraps
from typing import Optional, Dict, Any

import jwt
from flask import current_app, request, jsonify


def encode_auth_token(user_id: str) -> str:
    """
    Generates a JWT token.
    """
    payload = {
        "sub": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
    }
    token = jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256",
    )
    # PyJWT >= 2 returns a str already; older versions may return bytes
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def decode_auth_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET_KEY"],
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator to protect routes with JWT authentication.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid authorization header"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_auth_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token"}), 401

        user_id = payload.get("sub")
        if not user_id:
            return jsonify({"message": "Invalid token payload"}), 401

        # Inject user_id into kwargs
        kwargs["user_id"] = user_id
        return f(*args, **kwargs)

    return decorated
