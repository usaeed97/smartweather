# services/weather_api.py
import requests
from flask import current_app


def fetch_weather(city: str):
    """
    Call external weather API and return processed data.
    """
    base_url = current_app.config["WEATHER_API_BASE_URL"]
    api_key = current_app.config["WEATHER_API_KEY"]

    if not api_key:
        raise RuntimeError("WEATHER_API_KEY is not set")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    resp = requests.get(base_url, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()

    main = data.get("main", {})
    wind = data.get("wind", {})
    weather_list = data.get("weather", [])

    description = weather_list[0]["description"] if weather_list else "N/A"

    return {
        "city": data.get("name", city),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "wind_speed": wind.get("speed"),
        "description": description,
    }


def generate_alert(weather: dict) -> str:
    """
    Generate a simple alert based on temperature and wind speed.
    """
    temp = weather.get("temp")
    wind_speed = weather.get("wind_speed")

    if temp is not None and temp < 0:
        return "Freezing conditions: dress warmly!"
    if wind_speed is not None and wind_speed > 15:  # m/s ~ 54 km/h
        return "High wind alert: secure loose items."
    return "None"
