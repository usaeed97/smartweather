# routes/notes_routes.py
from flask import Blueprint, request, jsonify

from models.notes_model import (
    create_note,
    get_notes_by_user,
    get_note_by_id,
    update_note,
    delete_note,
)
from utils.auth import token_required

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes", methods=["POST"])
@token_required
def create_note_route(user_id):
    data = request.get_json() or {}
    city = data.get("city")
    note = data.get("note")
    rating = data.get("rating")

    if not city or not note or rating is None:
        return jsonify({"message": "city, note, and rating are required"}), 400

    try:
        rating = int(rating)
    except ValueError:
        return jsonify({"message": "rating must be an integer"}), 400

    note_id = create_note(user_id, city, note, rating)
    return jsonify({"message": "Note created", "note_id": note_id}), 201


@notes_bp.route("/notes", methods=["GET"])
@token_required
def list_notes(user_id):
    notes = get_notes_by_user(user_id)
    return jsonify(notes), 200


@notes_bp.route("/notes/<note_id>", methods=["GET"])
@token_required
def get_note_route(user_id, note_id):
    note = get_note_by_id(user_id, note_id)
    if not note:
        return jsonify({"message": "Note not found"}), 404
    return jsonify(note), 200


@notes_bp.route("/notes/<note_id>", methods=["PUT"])
@token_required
def update_note_route(user_id, note_id):
    data = request.get_json() or {}
    success = update_note(user_id, note_id, data)
    if not success:
        return jsonify({"message": "Note not found"}), 404
    return jsonify({"message": "Note updated"}), 200


@notes_bp.route("/notes/<note_id>", methods=["DELETE"])
@token_required
def delete_note_route(user_id, note_id):
    success = delete_note(user_id, note_id)
    if not success:
        return jsonify({"message": "Note not found"}), 404
    return jsonify({"message": "Note deleted"}), 200
