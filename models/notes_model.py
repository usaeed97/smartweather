# models/notes_model.py
from typing import List, Optional, Dict, Any
from bson import ObjectId
from .db import db

NOTES_COLLECTION = "notes"


def serialize_note(note: Dict[str, Any]) -> Dict[str, Any]:
    note["_id"] = str(note["_id"])
    note["user_id"] = str(note["user_id"])
    return note


def create_note(user_id: str, city: str, note: str, rating: int) -> str:
    result = db[NOTES_COLLECTION].insert_one(
        {
            "user_id": ObjectId(user_id),
            "city": city,
            "note": note,
            "rating": rating,
        }
    )
    return str(result.inserted_id)


def get_notes_by_user(user_id: str) -> List[Dict[str, Any]]:
    notes = db[NOTES_COLLECTION].find({"user_id": ObjectId(user_id)})
    return [serialize_note(n) for n in notes]


def get_note_by_id(user_id: str, note_id: str) -> Optional[Dict[str, Any]]:
    note = db[NOTES_COLLECTION].find_one(
        {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
    )
    if not note:
        return None
    return serialize_note(note)


def update_note(user_id: str, note_id: str, data: Dict[str, Any]) -> bool:
    update_fields = {}
    if "city" in data:
        update_fields["city"] = data["city"]
    if "note" in data:
        update_fields["note"] = data["note"]
    if "rating" in data:
        update_fields["rating"] = data["rating"]

    result = db[NOTES_COLLECTION].update_one(
        {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)},
        {"$set": update_fields},
    )
    return result.matched_count > 0


def delete_note(user_id: str, note_id: str) -> bool:
    result = db[NOTES_COLLECTION].delete_one(
        {"_id": ObjectId(note_id), "user_id": ObjectId(user_id)}
    )
    return result.deleted_count > 0
