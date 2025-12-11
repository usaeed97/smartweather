# routes/weather_routes.py
from flask import Blueprint, jsonify

from services.weather_api import fetch_weather, generate_alert

weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    """
    Public endpoint: fetch weather for a given city.
    """
    try:
        weather_data = fetch_weather(city)
        alert = generate_alert(weather_data)
        weather_data["alert"] = alert
        return jsonify(weather_data), 200
    except Exception as e:
        # In a real app, log the error
        return jsonify({"message": "Failed to fetch weather", "error": str(e)}), 502
