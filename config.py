# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()


class Config:
    # MongoDB Atlas URI or any cloud Mongo URI
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "smartweather")

    # JWT secret key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-change-me")

    # External Weather API settings (e.g. OpenWeatherMap)
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
    WEATHER_API_BASE_URL = os.getenv(
        "WEATHER_API_BASE_URL",
        "https://api.openweathermap.org/data/2.5/weather",
    )

    # Other settings can go here (debug, etc.)
    DEBUG = True
