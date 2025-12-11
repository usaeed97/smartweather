# models/user_model.py
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from .db import db


USERS_COLLECTION = "users"


def create_user(email: str, password: str):
    existing = db[USERS_COLLECTION].find_one({"email": email})
    if existing:
        return None  # user already exists

    hashed = generate_password_hash(password)
    result = db[USERS_COLLECTION].insert_one(
        {
            "email": email,
            "password": hashed,
        }
    )
    return str(result.inserted_id)


def get_user_by_email(email: str):
    user = db[USERS_COLLECTION].find_one({"email": email})
    if not user:
        return None
    user["_id"] = str(user["_id"])
    return user


def verify_user(email: str, password: str):
    user = db[USERS_COLLECTION].find_one({"email": email})
    if not user:
        return None
    if not check_password_hash(user["password"], password):
        return None
    user["_id"] = str(user["_id"])
    return user
